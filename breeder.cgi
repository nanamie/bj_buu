#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require "$datadir/profile.cgi";
#================================================
# 戦歴表示 Created by Merino
#================================================
&decode;
&header;
&header_profile;
&run;
&footer;
exit;
#================================================
sub run {
	open my $ifh, "< $userdir/$in{id}/pet_icon.cgi" or &error("$userdir/$in{id}/pet_icon.cgiﾌｧｲﾙが読み込めません");
	my $line = <$ifh>;
	close $ifh;

	my @data = split /<>/, $line;

	for my $pet (@data) {
		next unless $pet;
		my ($no, $icon, $lv, $exp) = split /;/, $pet;
		print qq|<li>Lv.$lv $pets[$no][1]</li><hr size="1">\n|;
	}
}
