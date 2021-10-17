#!/usr/bin/perl
use strict;
use warnings;
use Switch;
use Cwd;
use Getopt::Std;
use Data::Dumper;
use Ipvanish::Server;
use Ipvanish::City;

my @configs = ();
my @countries = (); 
my %cities; 
my @cities_found = ();
my @servers = ();
my $configs_dir = 'configs';

my %country_cities = ();
my %city_servers = ();

sub parse_configs{
  my $dir;
  opendir $dir, $configs_dir or die "Cannot open directory: $!";
    @configs = readdir $dir;
  closedir $dir;

  my @baddies;
  foreach(@configs){
    # ipvanish-US-Las-Vegas-las-c38.ovpn
    if($_ !~ /^.*\.ovpn$/m){
      push(@baddies, $_);
      next;
    }

    $_ =~ /(?:ipvanish-)(?<country>[A-Z]{2})-(?<city>[a-zA-Z-]*)-(?<city_short>[a-z]{3})-(?<server_id>[a-z][0-9]{2})(?:.ovpn)$/n;
    push(@countries, $+{country});
    push(@{$country_cities{$+{city_short}}}, $+{city});
    push(@{$city_servers{$+{city}}}, $+{server_id});
    if( grep( /$+{city_short}/, @cities_found ) ){
      $cities{$+{city_short}}->add_server($+{server_id});
    } else {
      push(@cities_found, $+{city_short});
      $cities{$+{city_short}} = City->new({
            country => $+{country},
            name => $+{city},
            abbv => $+{city_short}
          });
      $cities{$+{city_short}}->add_server($+{server_id});
    }
    push(@servers, Server->new({
          filepath => $_,
          name => $+{server_id},
          country => $+{country},
          city => $+{city},
          city_short => $+{city_short}
        }));
  }

  @countries = uniq(\@countries);
}

sub print_city_servers {
  my $city_short = shift @_;
  #print Dumper $cities{'atl'};
  if( not exists( $cities{$city_short} ) ){
    print "No such city: $city_short\n";
    return 1;
  }
  print "$city_short :\n";
  foreach( sort( @{$cities{$city_short}->{server_list}} ) ){
    print "$_ ";
  }
  print "\n";
  return 0;
}

sub uniq {
  # stderr_dk kindly requests $1M should this function become an NFT.
  my $ctrys = shift;
  my %seen;

  foreach ( @$ctrys ) {
      $seen{ $_ } = 1;
  }
  @$ctrys = reverse( sort ( keys ( %seen)));
}

sub get_all_country_abbv{
  print "Country codes: @countries\n";
}

sub do_args{
  switch($ARGV[0]){
    case "list" { return print_city_servers $ARGV[1]}
    case "countries" { get_all_country_abbv } 
    case "use" {}
    case "down" {}
    else { print "no\n" }
  }
}

parse_configs;
do_args;







