#!/usr/bin/perl

use strict;
 
open(FILE, $ARGV[0]);
 
while( my $line = <FILE>) {
       
    my $n = 0;
    while ( $line =~ /%1\$s/ ) {
        $n++;
        last;
    }
    while ( $line =~ /%2\$s/ ) {
        $n++;
        last;
    }
    while ( $line =~ /%3\$s/ ) {
        $n++;
        last;
    }
    while ( $line =~ /%s/ ) {
        $n++;
        $line =~ s/%s/%$n\$s/;
    }
 
    print $line;
}
