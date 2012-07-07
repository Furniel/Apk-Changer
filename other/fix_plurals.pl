#!/usr/bin/perl

use strict;
 
open(FILE, $ARGV[0]);
 
while( my $line = <FILE>) {
       
    my $n = 0;
    while ( $line =~ /%d/ ) {
        $n++;
        $line =~ s/%d/%$n\$d/;
    }  
 
    if ($n==1) {
        $line =~ s/%1\$d/%d/
    }  
 
    print $line;
}
