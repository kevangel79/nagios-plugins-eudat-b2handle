#!/usr/bin/perl

#
# Robert Verkerk  <robert.verkerk@surfsara.nl>, 2014
#
# This script is a nagios script to check if a handle is resolvable via all ip addresses and ports
#
# set ts:4
#

# Kyriakos Gkinis <kyrginis@admin.grnet.gr>, 2016 : add timeout option

#
use strict;
use warnings;
use Data::Dumper;
use Getopt::Long;
use JSON;
use Pod::Usage;
#

my $fullargv0 = $0;
my ($argv0) = $fullargv0 =~ /([^\/\\]+)$/;


########################################
# Settings
########################################
my $status=0;
my %settings = (
	'debug' => 'False',
	'handle' => {
				'prefix'	=> '0.NA',
				'siteinfo2'	=> 'http://lab.pidconsortium.eu/siteinfo2',
				'suffix'	=> 'EUDAT-B2HANDLE-CHECK',
				},
	);
my %data = ();

########################################
## Child processes 
########################################
my @children = ();

########################################
## Main
########################################

# process arguments
read_args(\%settings);

# get json info of a prefix
$status=retrievePrefixJsonInfo(\%settings, \%data);

# check the prefix ports 
if ( $status == 0 ) {
	$status=checkPrefixPorts(\%settings, \%data);
}

print Dumper \%data if $settings{debug} =~ /True/ ;

# return the status of the nagios check
$status=returnStatus(\%settings, \%data, $status);

exit($status);

#########################################
## Subroutines
#########################################

sub read_args {

	my $settings_ref = shift;
	my $help='';
	my $fullhelp='';
	my $debug='';
	my $timeout=0;

	#
	# process the options/arguments
	#
	GetOptions ('debug'			=> \$debug,
				'help'			=> \$help,
				'fullhelp'		=> \$fullhelp,
				'timeout=i'		=> \$timeout,
				'prefix=s'		=> \$settings_ref->{handle}->{prefix},
				'suffix=s'		=> \$settings_ref->{handle}->{suffix}
			   );

	if ( $debug ) {
		$settings_ref->{debug} = 'True';
	}
	if( $help ) {
		pod2usage(2);
	}
	if( $fullhelp ) {
		pod2usage(1);
	}

	if( $timeout > 0 ) { 
		$SIG{'ALRM'} = sub {
			kill ('TERM', @children);
			kill ('KILL', @children);
			print("UNKNOWN: Timeout reached, exiting\n");
			exit(3);
		};
		alarm($timeout);
	}

	return;	 
}

# Subroutine to GET all json info for a prefix
sub retrievePrefixJsonInfo {

	# Get the subroutine arguments
	my $settings_ref = shift;
	my $data_ref = shift;
	my $return_code=0;

	my $command = "curl -sSf --header \"application contents:json\" \"$settings_ref->{handle}->{siteinfo2}/$settings_ref->{handle}->{prefix}/servers/\" ";
	push @children, open( my $input_fh, "$command 2>&1 |" ) || die "Can't execute $command: $!";
	
	while ( defined( my $line = <$input_fh> ) ) {
		chomp $line;
		print "$line \n" if $settings_ref->{debug} =~ /True/ ;

		if ( $line =~ /\{*\}/ ) {
			# convert from json and put in correct place 
			my $json = JSON->new;
			$data_ref->{prefix}->{$settings_ref->{handle}->{prefix}} = $json->decode($line);
		} else {
			$return_code=2;
			push( @{$data_ref->{status}->{errorMessages}} , "$command"); 
			push( @{$data_ref->{status}->{errorMessages}} , "$line"); 
		}
	}

	close $input_fh;

	print Dumper $data_ref if $settings_ref->{debug} =~ /True/ ;

	return($return_code);
}

# Subroutine to check ports of a prefix
sub checkPrefixPorts {

	# Get the subroutine arguments
	my $settings_ref = shift;
	my $data_ref = shift;
	my $return_code=0;

	# loop over the prefixes
	foreach my $prefix ( keys %{$data_ref->{prefix}} ) {
		# check http info
		$return_code=checkPrefixHttpPort($settings_ref, $data_ref, $prefix);
	}

	return($return_code);
}

# Subroutine to check http ports of a prefix
sub checkPrefixHttpPort {

	# Get the subroutine arguments
	my $settings_ref = shift;
	my $data_ref = shift;
	my $prefix = shift;
	my $return_code=0;
	my $http_status="OK";

	# loop over the prefixes
	foreach my $ipAddress ( keys %{$data_ref->{prefix}->{$prefix}} ) {

		# construct parameters
		my $suffix=$settings_ref->{handle}->{suffix};
		
		if ( exists $data_ref->{prefix}->{$prefix}->{$ipAddress}->{interfaces}->{HTTP} ) {
			$data_ref->{status}->{httpPossible}+=1; 
			my $ipPort=$data_ref->{prefix}->{$prefix}->{$ipAddress}->{interfaces}->{HTTP};

			print "prefix: $prefix \tipaddress: $ipAddress \tport: $ipPort \n" if $settings_ref->{debug} =~ /True/ ;

			# check http info
			my $url="http://${ipAddress}:${ipPort}/${prefix}/${suffix}";
			my $command = "curl -sSf $url";
			push @children, open( my $input_fh, "$command 2>&1 |" ) || die "Can't execute $command: $!";
				
			while ( defined( my $line = <$input_fh> ) ) {
				chomp $line;
				print "$line \n" if $settings_ref->{debug} =~ /True/ ;
				if (( $line =~ /\<title\>Handle Not Found/ ) || ( $line =~ /curl/ )) {
					$return_code=1;
					push( @{$data_ref->{status}->{errorMessages}} , "$url is not present/reachable"); 
					if ( $line =~ /curl/ ) {
						push( @{$data_ref->{status}->{errorMessages}} , "$line"); 
					}
					$data_ref->{status}->{httpError}+=1; 
				}
			}
			close $input_fh;
		}
	}

	return($return_code);
}

# Subroutine to return the status of the checks
sub returnStatus {

	# Get the subroutine arguments
	my $settings_ref = shift;
	my $data_ref = shift;
	my $status = shift;
	my $return_code = 0;
	my $message = '';
	my $errorMessage = '';
	my $handle="$settings_ref->{handle}->{prefix}/$settings_ref->{handle}->{suffix}";

	# check the status. (0 == no errors. 0 != errors)
	if ( $status == 0 ) {
		print  "return_code = $return_code \n" if $settings_ref->{debug} =~ /True/ ;
		$message="OK, handle: $handle is reachable via all tested paths";
	} else {
		$message = "CRITICAL";
		$return_code = 2;
		print  "return_code = $return_code \n" if $settings_ref->{debug} =~ /True/ ;
		if (exists $data_ref->{status}->{httpPossible}) {
			if (exists $data_ref->{status}->{httpError}) {
				if ( $data_ref->{status}->{httpError} < $data_ref->{status}->{httpPossible} ) {
					$message="WARNING";
					$return_code = 1;
				} 
			}
		}

		$message="$message handle: $handle is NOT reachable via all tested paths";
		$errorMessage = join(', ',@{$data_ref->{status}->{errorMessages}});
		print "$errorMessage\n" if $settings_ref->{debug} =~ /True/ ;
	}

	print "$message |\n$errorMessage\n";

	return($return_code)

}
__END__
###############################################################################
# documentation
###############################################################################

=head1 NAME

check_handle_resolution.pl

=head1 SYNOPSIS

check_handle_resolution.pl B<--prefix> I<prefix list>  B<--suffix> I<suffix> B<--timeout> I<timeout>

check_handle_resolution.pl B<--prefix> I<prefix list>  B<--suffix> I<suffix> --debug

check_handle_resolution.pl B<--prefix> I<prefix list>

check_handle_resolution.pl B<--help>


----------------

Please use --fullhelp for explanation of all options

=head1 DESCRIPTION

This program can be used to to check the reachability of handle servers.

The procedure works as follows:
	It retrieves all masters and mirrors of a prefix.
	Than it loops over all ip addresses and ports to check if a predefined handle is readable
	The status is given back in nagios format

=head1 OPTIONS

=over 4

=item B<--debug, -d>

Debug mode. Be verbose in what is being done and what the results of subroutines is.

=item B<--help, -h>

Show this help text

=item B<--timeout, -t> I<timeout>

Timeout after I<timeout> seconds

=item B<--prefix, -p> I<prefix list>

Use the supplied prefix instead of 0.NA to check

=item B<--suffix, -s> I<suffix>

Use the supplied suffix instead of 'EUDAT-B2HANDLE-CHECK' to check

=back

=head1 EXAMPLES

=over 4

=item B<prefix>

use the supplied prefix to check.

C<check_handle_resolution.pl --prefix 10916>

=item B<suffix>

use the supplied suffix to check.

C<check_handle_resolution.pl --suffix bladiebla>

=back

=head1 AUTHOR

Robert Verkerk <robert.verkerk@surfsara.nl>

Copyright (c) 2014-2015 by Robert Verkerk

=head1 VERSION

Version 0.2 (January 2015)

=back

=cut
