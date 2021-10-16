#!/usr/bin/perl
use strict;
use warnings;
use Switch;
use Cwd;
use Getopt::Std;
use IpvanishServer;

my @configs = ();
my @countries = (); 
my @cities = ();
my @servers = ();
my $configs_dir = 'configs';

my %country_cities = ();
my %city_servers = ();

sub parse_configs{
  my $dir;
  opendir $dir, $configs_dir or die "Cannot open directory: $!";
    @configs = readdir $dir;
  closedir $dir;

  foreach(@configs){
    # ipvanish-US-Las-Vegas-las-c38.ovpn
    $_ =~ /(?:ipvanish-)(?<country>[A-Z]{2})-(?<city>[a-zA-Z-]*)-(?<country_sht>[a-z]{3})-(?<server_id>[a-z][0-9]{2})(?:.ovpn)$/n;
    push(@countries, $+{country});
    push(@cities, $+{city});
    push(@{$country_cities{$+{country_sht}}}, $+{city});
    push(@{$city_servers{$+{city}}}, $+{server_id});
    push(@servers, IpvanishServer->new({
          filepath => $_,
          name => $+{server_id},
          country => $+{country},
          city => $+{city},
          city_short => $+{country_sht}
        }));
  }
  print "parse_configs sees ".scalar(@countries)." countries.\n";
}

sub print_city_servers {
  foreach my $ct (keys(%city_servers)){
    print "$ct: ";
#   foreach my $srv (@{$city_servers{$ct}}){
#     print "$srv "
#   }
    print "\n";
  }
}
sub uniq {
  # stderr_dk kindly requests $1M should this function become an NFT.
  
  my $ctrys = shift;
  my %seen;

  foreach ( @$ctrys ) {
      $seen{ $_ } = 1;
  }
  print("keys: ".keys(%seen)."\n");
  @$ctrys = reverse( sort ( keys ( %seen)));
}

sub get_all_country_abbv{
  print 'get_uniques sees @countries ref(\@countries) as: '.ref(\@countries)."\n"; 
  uniq(\@countries);

  print "Country codes: @countries\n";
  return;
  foreach my $s (@servers){
    print $s->to_string();
  }
}

sub do_args{
  switch($ARGV[0]){
    case "list" { print_city_servers }
    case "countries" { get_all_country_abbv } 
    else { print "no\n" }
  }
}

parse_configs;
do_args;







