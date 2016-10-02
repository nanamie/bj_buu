require './lib/add_collection.cgi';
#=================================================
# ｺﾚｸｼｮﾝﾙｰﾑ Created by Merino
#=================================================

# ｺﾚｸｼｮﾝﾀｲﾄﾙ,legendﾌｧｲﾙ,一時的称号
my @collections = (
	['武器図鑑', 'comp_wea', '★最終兵器'],
	['ﾀﾏｺﾞ図鑑', 'comp_egg', '★ｴｯｸﾞﾏﾝ'],
	['ﾍﾟｯﾄ図鑑', 'comp_pet', '★ﾍﾟｯﾄ牧場'],
	['防具図鑑', 'comp_gua', '★防衛装置'],
);


#=================================================
sub begin {	
	$layout = 2;
	my @lines = &add_collection;
	my $kind = 1;
	for my $line (@lines) {
		$line =~ tr/\x0D\x0A//d;
		
		my $count = 0;
		my $sub_mes  = '';
		for my $no (split /,/, $line) {
			next if $no eq ''; # 先頭の空
			next if $kind == 2 && $no == 53;
			next if $kind == 3 && $no == 180;
			next if $kind == 3 && $no == 181;
			next if $kind == 3 && $no == 195;
			++$count;
			next unless $no;
			$sub_mes .= $kind eq '1' ? "<li>[$weas[$no][2]]$weas[$no][1]</li>"
					  : $kind eq '2' ? "<li>$eggs[$no][1]</li>"
					  : $kind eq '3' ? "<li>$pets[$no][1]</li>"
					  :                "<li>[$guas[$no][2]]$guas[$no][1]</li>"
					  ;
		}
		
		my $comp_par = 0;
		if ($count > 0) {
			if ($kind eq '1') {
				$comp_par = int($count / $#weas * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq $#weas;
			}
			elsif ($kind eq '2') {
				$comp_par = int($count / ($#eggs - 1) * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq ($#eggs - 1);
			}
			elsif ($kind eq '3') {
				$comp_par = int($count / ($#pets - 4) * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq ($#pets - 4);
			}
			elsif ($kind eq '4') {
				$comp_par = int($count / ($#guas - 4) * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq ($#guas - 4);
			}
		}
		
		$mes .= "$collections[$kind-1][0] 《ｺﾝﾌﾟ率 $comp_par%》<br>";
		$mes .= "<ul> $sub_mes </ul>";
		
		++$kind;
	}
	
	&refresh;
	&n_menu;
}

#=================================================
# ｺﾝﾌﾟﾘｰﾄ処理
#=================================================
sub write_comp_legend {
	my $kind = shift;
	
	&write_legend($collections[$kind-1][1], "$c_mの$m{name}が$collections[$kind-1][0]をｺﾝﾌﾟﾘｰﾄする", 1);
	&mes_and_world_news("<i>$collections[$kind-1][0]をｺﾝﾌﾟﾘｰﾄしました。$m{name}に$collections[$kind-1][2]の称号があたえられました</i>");
	
	# 一時的な称号
	$m{shogo} = $collections[$kind-1][2];

	$kind--;
	# 0 を追加することで 100%を超えることになり
	my @lines = ();
	open my $fh, "+< $userdir/$id/collection.cgi" or &error("ｺﾚｸｼｮﾝﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($kind eq @lines) {
			$line =~ tr/\x0D\x0A//d; # \n改行削除
			$line .= "0,\n";
		}
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # 削除不可
