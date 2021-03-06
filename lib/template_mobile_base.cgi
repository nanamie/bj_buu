#================================================
# 携帯ｹﾞｰﾑ画面 Created by Merino
#================================================

#================================================
# ﾒｲﾝ
#================================================
print qq|資金 $m{money} G<br>| if $m{lib} =~ /^shopping/ || $m{lib_r} =~ /^shopping/;
#print qq|<a name="menu">$menu_cmd</a><br>$mes<br>|;
print qq|<a name="menu">$menu_cmd</a>$mes$tutorial_mes|;

if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif ($m{lib} eq '' || $m{lib} eq 'prison') {
	&check_flag;
	&show_world_news;
	&status_html;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}
elsif ($m{wt} > 0) {
	&check_flag;
	&show_world_news;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}
elsif ($m{lib} =~ /(domestic|hunting|military|promise|training|war_form)/ && $m{tp} eq '1') {
	print qq|<hr>|;
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]★$m{pet_c}</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)</font><br>|; }
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
}

#================================================
# ﾄｯﾌﾟﾒﾆｭｰ
#================================================
sub top_menu_html {
	print qq|<hr><a href="$script_index" accesskey="0">0.TOP</a>/| unless $m{disp_top} eq '0';
	print qq|<a href="./news.cgi?id=$id&pass=$pass" accesskey="1">1.過去の栄光</a>/| unless $m{disp_news} eq '0';
	print qq|<a href="./bbs_public.cgi?id=$id&pass=$pass" accesskey="2">2.掲示板</a>/|;
	print qq|<a href="./chat_public.cgi?id=$id&pass=$pass" accesskey="3">3.交流広場</a>/| unless $m{disp_chat} eq '0';
	print qq|<a href="./chat_horyu.cgi?id=$id&pass=$pass">改造案投票所</a>/|;
	print qq|<a href="./bbs_ad.cgi?id=$id&pass=$pass" accesskey="4">4.宣伝言板</a>/| unless $m{disp_ad} eq '0';
	print qq|<a href="./letter.cgi?id=$id&pass=$pass" accesskey="5">5.MyRoom</a>/|;
	print qq|<a href="./chat_prison.cgi?id=$id&pass=$pass" accesskey="7">7.牢獄</a>/|;
	print qq|<a href="./bbs_country.cgi?id=$id&pass=$pass" accesskey="8">8.作戦会議</a>/|;
	print qq|<a href="./bbs_union.cgi?id=$id&pass=$pass" accesskey="9">9.同盟会議</a>/| if $union;
	print qq|<a href="./bbs_vs_npc.cgi?id=$id&pass=$pass" accesskey="6">6.+封印会議+</a>/| if ($w{world} eq $#world_states) && $m{country} ne $w{country};
#	print qq|<a href="./bbs_akindo.cgi?id=$id&pass=$pass" accesskey="*">*.ギルド</a>/| if $m{akindo_guild};
	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		print $a_line;
	}
	print qq|<a href="./chat_casino.cgi?id=$id&pass=$pass">対人ｶｼﾞﾉ</a>/|;
	print qq|<a href="./bbs_daihyo.cgi?id=$id&pass=$pass">代表\評議会</a>/| unless $m{disp_daihyo} eq '0';
	print qq|<a href="./chat_admin.cgi?id=$id&pass=$pass">運営討論場</a>/| if (&is_sabakan);
}

#================================================
# ｽﾃｰﾀｽ画面
#================================================
sub status_html {
	print qq|<hr><img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|<img src="$icondir/pet/$m{icon_pet}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon_pet} && $m{pet_icon_switch};
	print qq|$m{name}|;
	print qq|[$m{shogo}]| if $m{shogo};
	print qq|<br>|;
#	print $m{name}, "[$m{shogo}]<br>";
#	print qq|称号 $m{shogo}<br>| if $m{shogo};

	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	if ($m{master}){
		if($m{master_c}){
			print qq|師匠 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
		}else{
			$mid = unpack 'H*', $m{master};
			if (-f "$userdir/$mid/user.cgi") {
				$master = qq|弟子 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
			} else {
				$master = qq|弟子 <font color="#FF0000">$m{master} 死亡</font><br>|;
			}
		}
	}
	print qq|<b>$m{sedai}</b>世代目 $sexes[$m{sex}]<br>|;
#	print qq|Lv.<b>$m{lv}</b><br>|;
	print qq|Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>|;
	print qq|疲労度 <b>$m{act}</b>%<br>|;
	print qq|経験値 [<b>$m{exp}</b>/<b>100</b>]<br>|;
	print qq|資金 <b>$m{money}</b> G<br>|;
	print qq|<font color="#CC9999">$e2j{hp} [<b>$m{hp}</b>/<b>$m{max_hp}</b>]</font><br>|;
	print qq|<font color="#CC99CC">$e2j{mp} [<b>$m{mp}</b>/<b>$m{max_mp}</b>]</font><br>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<font color="#9999CC">武器:[$weas[$m{wea}][2]]$wname★<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>| if $m{wea};
	print qq|<font color="#9999CC">防具:[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>| if $m{gua};
	my $icon_pet_lv = " Lv.<b>$m{icon_pet_lv}</b>" if $m{icon_pet} && $m{pet_icon_switch};
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]★$m{pet_c}$icon_pet_lv</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)$icon_pet_lv</font><br>|; }
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print qq|<font color="#CCCC99">虫:$m{insect_name}</font><br>| if $m{insect_name};
}

#================================================
# 手紙、荷物ﾁｪｯｸ
#================================================
sub check_flag {
	if (-f "$userdir/$id/temp_mes.cgi") {
		open my $fh, "< $userdir/$id/temp_mes.cgi";
		my $line = <$fh>;
		close $fh;
		print qq|<hr><font color="#FF0000">$line</font><br>|;
	}
	if ($m{tutorial_switch}) {
		print qq|<hr><font color="#FF0000">ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞ</font><br>|;
	}
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi";
		my $line = <$fh>;
		my($letters) = split /<>/, $line;
		close $fh;
		print qq|<hr><font color="#FFCC66">手紙が $letters 件届いています</font><br>| if $letters;
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		print qq|<hr><font color="#FFCC00">預かり所に荷物が届いています</font><br>|;
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		print qq|<font color="#FFCC99">ﾏｲﾙｰﾑに荷物が届いています</font><br>|;
	}
	my $is_breeder_find = 0;
	for my $bi (0 .. 2) {
		if (-f "$userdir/$id/shopping_breeder_$bi.cgi") {
			if ((stat "$userdir/$id/shopping_breeder_$bi.cgi")[9] < $time) {
				$is_breeder_find = 1;
			}
		}
	}
	print qq|<font color="#FF66CC">育て屋の卵が孵化しています</font><br>| if $is_breeder_find;
}

#================================================
# 戦闘画面
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';
	
	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $m_tokkou2 = $is_m_tokkou2 ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou2 = $is_y_tokkou2 ? '<font color="#FFFF00">★</font>' : '';

	print "$m_icon$m{name}$m_mes<br>";
	print "$e2j{hp}(<b>$m{hp}</b>/<b>$m{max_hp}</b>)/$e2j{mp}(<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br>";
	print "攻撃[<b>$m_at</b>]/防御[<b>$m_df</b>]/素早[<b>$m_ag</b>]<br>";
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print "$m_tokkou武器:[$weas[$m{wea}][2]]$wname★$m{wea_lv}($m{wea_c})<br>" if $m{wea};
	print "$m_tokkou2防具:[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>" if $m{gua};
	print "ﾍﾟｯﾄ:$pets[$m{pet}][1]★$m{pet_c}<br>" if $pets[$m{pet}][2] eq 'battle';
	print "Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>";
	print "疲労度 <b>$m{act}</b>%<br>";
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print "<hr>";
	print "$y_icon$y{name}$y_mes<br>";
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	print "$e2j{hp}(<b>$y{hp}</b>/<b>$y{max_hp}</b>)/$e2j{mp}(<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br>";
	print "攻撃[<b>$y_at</b>]/防御[<b>$y_df</b>]/素早[<b>$y_ag</b>]<br>";
	print "$y_tokkou武器:[$weas[$y{wea}][2]]$ywname<br>" if $y{wea};
	print "$y_tokkou2防具:[$guas[$y{gua}][2]]$guas[$y{gua}][1]<br>" if $y{gua};
}

#================================================
# 戦争画面
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';
	
	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	
	print qq|$m_icon<font color="$cs{color}[$m{country}]">$m{name}$m_mes</font><br>|;
	print qq|$m_tokkou$units[$m{unit}][1]/<b>$m{sol}</b>兵/士気[<b>$m{sol_lv}</b>%]/統率[<b>$m_lea</b>]<br>|;
	print qq|<hr>|;
	print qq|$y_icon<font color="$cs{color}[$y{country}]">$y{name}$y_mes</font><br>|;
	print qq|$y_tokkou$units[$y{unit}][1]/<b>$y{sol}</b>兵/士気[<b>$y{sol_lv}</b>%]/統率[<b>$y_lea</b>]<br>|;
}

#================================================
# 自国/同盟国の情報
#================================================
sub my_country_info {
	my $next_rank = $m{rank} * $m{rank} * 10;
	my $nokori_time = $m{next_salary} - $time;
	$nokori_time = 0 if $nokori_time < 0;
	my $gacha_time = $m{gacha_time} - $time;
	$gacha_time = 0 if $gacha_time < 0;
	my $gacha_time2 = $m{gacha_time2} - $time;
	$gacha_time2 = 0 if $gacha_time2 < 0;
	my $offertory_time = $m{offertory_time} - $time;
	$offertory_time = 0 if $offertory_time < 0;

	print qq|<hr>|;
	print qq|$units[$m{unit}][1] <b>$rank_sols[$m{rank}]</b>兵<br>|;
	my $rank_name = &get_rank_name($m{rank}, $m{name});
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '★' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	print qq|$rank_name $e2j{rank_exp} [<b>$m{rank_exp}/$next_rank</b>]<br>|;
	print qq|敵国<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font>連続<b>$m{renzoku_c}</b>回<br>| if $m{renzoku_c};
	printf ("次の給与<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後<br>", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
	if ($m{disp_gacha_time}) {
		printf ("次のガチャ<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後<br>", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		printf ("次のガチャ（高級）<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後<br>", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		printf ("次の賽銭<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後<br>", $offertory_time / 3600, $offertory_time % 3600 / 60, $offertory_time % 60);
	}
	print qq|<hr><font color="$cs{color}[$m{country}]">$c_m</font><br>|;
	print qq|$e2j{strong}:$cs{strong}[$m{country}]<br>|;
	print qq|$e2j{tax}:$cs{tax}[$m{country}]%<br>|;
	print qq|$e2j{state}:$country_states[ $cs{state}[$m{country}] ]<br>|;
	print qq|$e2j{food}:$cs{food}[$m{country}]<br>|;
	print qq|$e2j{money}:$cs{money}[$m{country}]<br>|;
	print qq|$e2j{soldier}:$cs{soldier}[$m{country}]<br>|;

	if ($union) {
		print qq|<hr><font color="$cs{color}[$union]">$cs{name}[$union]</font><br>|;
		print qq|$e2j{strong}:$cs{strong}[$union]<br>|;
		print qq|$e2j{tax}:$cs{tax}[$union]%<br>|;
		print qq|$e2j{state}:$country_states[ $cs{state}[$union] ]<br>|;
		print qq|$e2j{food}:$cs{food}[$union]<br>|;
		print qq|$e2j{money}:$cs{money}[$union]<br>|;
		print qq|$e2j{soldier}:$cs{soldier}[$union]<br>|;
	}
}

#================================================
# 各国国力の情報
#================================================
sub countries_info {
	print  "<hr>各国の$e2j{strong}<br>";
	for my $i (1 .. $w{country}) {
		print qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		my $status = $cs{strong}[$i];
		if ($cs{is_die}[$i] == 1) {
			$status = "滅亡";
		}
		elsif ($cs{is_die}[$i] == 2) {
			$status = "鎖国";
		}
		elsif ($cs{is_die}[$i] == 3) {
			$status = "崩壊";
		}
		print $w{world} eq '10' ? '' : $status;

#		print $w{world} eq '10' ? ''
#			: $cs{is_die}[$i]   ? "滅亡"
#			:                     "$cs{strong}[$i]"
#			;
		

		print "[$cs{barrier}[$i]%]"; # 城壁値

		if ($m{country} && $m{country} ne $i) {
			my $c_c = &union($m{country}, $i);
			print qq|[$w{'f_'.$c_c}%]|;
			if   ($w{'p_'.$c_c} eq '1') { print qq|<font color="#009900">同盟</font>|; }
			elsif($w{'p_'.$c_c} eq '2') { print qq|<font color="#FF0000">交戦</font>|; }
		}
		print "<br>";
	}

	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . '時間' : int($limit_hour / 24) . '日';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>時間<b>%02d</b>分<b>%02d</b>秒後", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<hr><font color="#FF0000">●</font>| : qq|<hr><font color="#00FF00">●</font>|;
	print qq|ﾌﾟﾚｲ中 $w{playing}/$max_playing人|;
	print qq|<hr>統一期限 残り$limit_day<br>|;
	if ($reset_rest > 0){
		print qq|終戦期間【残り$reset_time_mes】<br>|;
	}
	print qq|難易度 Lv.$w{game_lv}<br>統一$e2j{strong} $touitu_strong<br>| unless $w{world} eq '10';
	print $c2 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>同盟<br>|
		: $c1 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><br>|
		:       ''
		;
	print qq|世界情勢 <a href="world_summaries.cgi?id=$id&pass=$pass&world=$w{world}" style="color:inherit;text-decoration:none;">$world_states[$w{world}]</a><br>|;
	print qq|$world_name暦$w{year}年<br>|;
}

#================================================
# ｶｼﾞﾉの人数
#================================================
sub all_member_n {
	my $ret_str = '';
	my $ret_str2 = '';
	my $casino_n_file = "$logdir/casino_n.cgi";
	my $lastmodified = (stat $casino_n_file)[9];

	if (($lastmodified + 180) < $time) { # 3分毎に対人ｶｼﾞﾉの人数更新
		for my $i (0 .. $#files) {
			my $member_c  = 0;
			my %sames = ();
			my $tf_name = "$logdir/chat_casino$files[$i][2]_member.cgi";
			open my $fh, "< $tf_name" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
			my $head_line = <$fh>;
			while (my $line = <$fh>) {
				my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
				next if ($time - 180) > $mtime;
				next if $sames{$mname}++; # 同じ人なら次
				$member_c++;
			}
			close $fh;
			$ret_str2 .= substr($files[$i][0], 0, 2) . "/$member_c <>";
		}
		open my $fh, "> $casino_n_file" or &error('対人ｶｼﾞﾉの人数ﾌｧｲﾙが開けません');
		print $fh $ret_str2;
		close $fh;
	}
	else {
		open my $fh, "< $casino_n_file" or &error('対人ｶｼﾞﾉの人数ﾌｧｲﾙが開けません');
		$ret_str2 = <$fh>;
		close $fh;
	}
	my @casinos_n = split /<>/, $ret_str2;
	for my $i (0 .. $#casinos_n) {
		$ret_str .= $casinos_n[$i];
	}

	return $ret_str;
}

sub show_world_news {
	open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiﾌｧｲﾙが読み込めません");
	my $line = <$fh>;
	close $fh;
	print "<hr>$line<hr>";

	# ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞ時のｸｴｽﾄ情報
	if ($m{tutorial_switch}) {
		require './lib/tutorial.cgi';
		if ($m{country} == 0) { # ﾈﾊﾞﾗﾝでは仕官催促固定
			print qq|「国情報」→「仕官」から国を選ぶことで仕官できます<hr>|;
		}
		elsif ($m{tutorial_quest_stamp_c} < $tutorial_quest_stamps) {
			my $quest = &show_quest;
			print qq|$quest<hr>|;
		}
	}
}

1; # 削除不可
