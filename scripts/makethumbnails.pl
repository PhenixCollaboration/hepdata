#!/usr/bin/perl
@pngs = `ls *.png`;
for($i=0; $i<=$#pngs;$i++){
chomp($pngs[$i]);
$out = "thumb\_$pngs[$i]";
system "cp $pngs[$i] $out\n";
}
