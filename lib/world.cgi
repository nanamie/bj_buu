sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
require './lib/_world_reset.cgi';
#================================================
# 世界情勢 Created by Merino
#================================================

#================================================
# 選択画面
#================================================
sub tp_100 {
	$mes .= "あなたはこの世界に何を求めますか?<br>";
	&menu('皆が望むもの','希望','絶望','平和');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};
	require './lib/_festival_world.cgi';
#	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
#	my $wline;
#	$wline = <$fh>;
#	my @old_worlds = split /<>/, $wline;
#	close $fh;
#	my @next_worlds;
	my @new_worlds;
	
	if ($cmd eq '1') { # 希望
		&mes_and_world_news("<b>世界に希望を望みました</b>", 1);
		@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
	}
	elsif ($cmd eq '2') { # 絶望
		&mes_and_world_news("<b>世界に絶望を望みました</b>", 1);
		@new_worlds = (8,9,10,11,12,13,14,15,16);
	}
	elsif ($cmd eq '3') { # 平和
		&mes_and_world_news("<b>世界に平和を望みました</b>", 1);
		@new_worlds = (0);
	}
	else {
		&mes_and_world_news('<b>世界にみなが望むものを望みました</b>', 1);
		@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
	}

#	for my $new_v (@new_worlds){
#		my $old_year = 0;
#		my $old_flag = 0;
#		for my $o (@old_worlds){
#			last if $old_year > 10;
#			if ($new_v == $o){
#				$old_flag = 1;
#				last;
#			}
#			$old_year++;
#		}
#		push @next_worlds, $new_v unless $old_flag;
#	}
	my @next_worlds = &unique_worlds(@new_worlds);

	$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
	$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

	# 強制暗黒期
	if ($old_world eq $#world_states) {
		$w{world} = $#world_states;
		&write_world_news("<i>$m{name}の願いはかき消されました</i>");
	}
	# 強制シャッフル
	elsif ($old_world eq $#world_states-1) {
		$w{world} = $#world_states-1;
		&write_world_news("<i>$m{name}の願いは空しく世界は混乱に陥りました</i>");
	}
	# 強制紅白
	elsif ($old_world eq $#world_states-2) {
		$w{world} = $#world_states-2;
		&write_world_news("<i>$m{name}の願いは空しく世界は二つに分かれました</i>");
	}
	# 強制三国
	elsif ($old_world eq $#world_states-3) {
		$w{world} = $#world_states-3;
		&write_world_news("<i>$m{name}の願いも空しく分裂した世界を統一すべく三国が台頭しました</i>");
	}
	# 強制英雄
	elsif ($old_world eq $#world_states-4) {
		$w{world} = $#world_states-4;
		&write_world_news("<i>$m{name}の願いは空しく世界は英雄が伝説を作り出す時代になりました</i>");
	}
	# 強制拙速
	elsif ($old_world eq $#world_states-5) {
		$w{world} = $#world_states-5;
		&write_world_news("<i>$m{name}の願いも空しく世界が競い合うことに</i>");
	}
	# 同じのじゃつまらないので
	elsif ($w{world} eq $old_world) {
		$w{world} = int(rand(@world_states-3));
		++$w{world} if $w{world} eq $old_world;
		$w{world} = int(rand(10)) if $w{world} > $#world_states-3;
		&write_world_news("<i>世界は $world_states[$old_world] となりま…せん $world_states[$w{world}]となりました</i>");
	}
	else {
		if ($w{world} eq '0') { # 平和
			&write_world_news("<i>世界は $world_states[$w{world}] になりました</i>");
		}elsif ($w{world} eq '18') { # 殺伐
			&write_world_news("<i>世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました</i>");
		}else{
			&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
		}
	}	
	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$nline\n";
	close $fh;
	
	my $migrate_type = 0;
	if ($w{world} eq '0') { # 平和
		$w{reset_time} += 3600 * 12;
	}
	elsif ($w{world} eq '6') { # 結束
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# 奇数の場合は一番国は除く
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	elsif ($w{world} eq '18') { # 殺伐
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states-4) { # 英雄
		$w{game_lv} += 20;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states-2) { # 不倶戴天
		$w{game_lv} = 99;
		$w{country} += 2;
		my $max_c = int($w{player} / 2) + 3;
		for my $i ($w{country}-1..$w{country}){
			mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
			for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				next if -f $output_file;
				open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
				close $fh;
				chmod $chmod, $output_file;
			}
			for my $file_name (qw/leader member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
				close $fh;
				chmod $chmod, $output_file;
			}
			&add_npc_data($i);
			# create union file
			for my $j (1 .. $i-1) {
				my $file_name = "$logdir/union/${j}_${i}";
				$w{ "f_${j}_${i}" } = -99;
				$w{ "p_${j}_${i}" } = 2;
				next if -f "$file_name.cgi";
				open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
				close $fh;
				chmod $chmod, "$file_name.cgi";
				open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
				close $fh2;
				chmod $chmod, "${file_name}_log.cgi";
				open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
				close $fh3;
				chmod $chmod, "${file_name}_member.cgi";
			}
			unless (-f "$htmldir/$i.html") {
				open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
				close $fh_h;
			}
			$cs{name}[$i]     = $i == $w{country} ? "たけのこの里":"きのこの山";
			$cs{color}[$i]    = $i == $w{country} ? '#ff0000':'#ffffff';
			$cs{member}[$i]   = 0;
			$cs{win_c}[$i]    = 999;
			$cs{tax}[$i]      = 99;
			$cs{strong}[$i]   = 75000;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = $max_c;
			$cs{is_die}[$i]   = 0;
			my @lines = &get_countries_mes();
			if ($w{country} > @lines - 2) {
				open my $fh9, ">> $logdir/countries_mes.cgi";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				close $fh9;
			}
		}
		$migrate_type = festival_type('kouhaku', 1);
		
		for my $i (1 .. $w{country}-2) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-2) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	elsif ($w{world} eq $#world_states-3) { # 三国志
		$w{game_lv} = 99;
		$w{country} += 3;
		my $max_c = int($w{player} / 3) + 3;
		for my $i ($w{country}-2..$w{country}){
			mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
			for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				next if -f $output_file;
				open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
				close $fh;
				chmod $chmod, $output_file;
			}
			for my $file_name (qw/leader member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
				close $fh;
				chmod $chmod, $output_file;
			}
			&add_npc_data($i);
			# create union file
			for my $j (1 .. $i-1) {
				my $file_name = "$logdir/union/${j}_${i}";
				$w{ "f_${j}_${i}" } = -99;
				$w{ "p_${j}_${i}" } = 2;
				next if -f "$file_name.cgi";
				open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
				close $fh;
				chmod $chmod, "$file_name.cgi";
				open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
				close $fh2;
				chmod $chmod, "${file_name}_log.cgi";
				open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
				close $fh3;
				chmod $chmod, "${file_name}_member.cgi";
			}
			unless (-f "$htmldir/$i.html") {
				open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
				close $fh_h;
			}
			$cs{name}[$i]     = $i == $w{country}-2 ? '魏':
								$i == $w{country}-1 ? '呉':
													'蜀';
			$cs{color}[$i]    = $i == $w{country}-2 ? '#4444ff':
								$i == $w{country}-1 ? '#ff4444':
													'#44ff44';
			$cs{member}[$i]   = 0;
			$cs{win_c}[$i]    = 999;
			$cs{tax}[$i]      = 99;
			$cs{strong}[$i]   = 50000;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = $max_c;
			$cs{is_die}[$i]   = 0;
			my @lines = &get_countries_mes();
			if ($w{country} > @lines - 3) {
				open my $fh9, ">> $logdir/countries_mes.cgi";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				close $fh9;
			}
		}
		$migrate_type = festival_type('sangokusi', 1);
		for my $i (1 .. $w{country}-3) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-2) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	elsif ($w{world} eq $#world_states-5) { # 拙速
		$migrate_type = festival_type('sessoku', 1);
	}
	elsif ($w{world} eq $#world_states-1) { # 混乱
		$migrate_type = festival_type('konran', 1);
	}
	
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	
	&refresh;
	&n_menu;
	&write_cs;
	
	require "./lib/reset.cgi";
	&player_migrate($migrate_type);
}

1; # 削除不可
