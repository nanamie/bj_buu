sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
#require './lib/reset.cgi';
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

	if ($cmd eq '1') { # 希望
		&mes_and_world_news("<b>世界に希望を望みました</b>", 1);
	}
	elsif ($cmd eq '2') { # 絶望
		&mes_and_world_news("<b>世界に絶望を望みました</b>", 1);
	}
	elsif ($cmd eq '3') { # 平和
		&mes_and_world_news("<b>世界に平和を望みました</b>", 1);
	}
	else {
		&mes_and_world_news('<b>世界にみなが望むものを望みました</b>', 1);
	}
	if (&is_special_world) { # 特殊情勢の開始時
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 英雄
			&write_world_news("<i>$m{name}の願いは空しく世界は英雄が伝説を作り出す時代になりました</i>");
		}
		elsif ($w{year} =~ /6$/) { # 暗黒
			&write_world_news("<i>$m{name}の願いはかき消されました</i>");
		}
		elsif ($w{year} % 40 == 0) { # 不倶戴天
			&write_world_news("<i>$m{name}の願いは空しく世界は二つに分かれました</i>");
		}
		elsif ($w{year} % 40 == 20) { # 三国志
			&write_world_news("<i>$m{name}の願いも空しく分裂した世界を統一すべく三国が台頭しました</i>");
		}
		elsif ($w{year} % 40 == 10) { # 拙速
			&write_world_news("<i>$m{name}の願いも空しく世界が競い合うことに</i>");
		}
		else { # 混乱
			&write_world_news("<i>$m{name}の願いは空しく世界は混乱に陥りました</i>");
		}
	}
	else { # 特殊情勢以外の開始時
		my @new_worlds;
		if ($cmd eq '1') { # 希望
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') { # 絶望
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') { # 平和
			@new_worlds = (0);
		}
		else {
			@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
		my @next_worlds = &unique_worlds(@new_worlds);
		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# 同じのじゃつまらないので
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>世界は $world_states[$old_world] となりま…せん $world_states[$w{world}]となりました</i>");
		}
		else {
			&opening_common;
		}
		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else { # 特殊情勢以外の開始時

	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;
}

1; # 削除不可