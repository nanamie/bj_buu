$mes .= qq|ｺｲﾝ $m{coin} 枚<br>| if ($is_mobile || $is_smart);
#================================================
# ｶｼﾞﾉ Created by Merino
#================================================
# @m…mark @o…ozz の意味
$base_bet = 10;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方は出入り禁止です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かやっちゃう?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "いらっしゃ〜い♪ｼﾞｬﾝｼﾞｬﾝ遊んでいってね<br>";
	}
	
#	&menu('やめる','$1ｽﾛｯﾄ','$10ｽﾛｯﾄ','$100ｽﾛｯﾄ','ﾊｲﾛｳ','ﾄﾞｯﾍﾟﾙ','ﾌﾞﾗｯｸｼﾞｬｯｸ','ﾎﾟｰｶｰ','ﾋｯﾄｱﾝﾄﾞﾌﾞﾛｰ','ﾊｲﾛｳ2');
	&menu('やめる','$1ｽﾛｯﾄ','$10ｽﾛｯﾄ','$100ｽﾛｯﾄ','$1000ｽﾛｯﾄ','ﾊｲﾛｳ','ﾄﾞｯﾍﾟﾙ','ﾌﾞﾗｯｸｼﾞｬｯｸ','ﾎﾟｰｶｰ','準備中','ﾊｲﾛｳ2','裏ﾄﾞｯﾍﾟﾙ','ﾛｲﾔﾙﾎﾟｰｶｰ');
}

sub tp_1 {
	return if &is_ng_cmd(1..12);
	
	$m{tp} = $cmd * 100;
	&menu('Play!', 'やめる');
	$m{stock} = 0;
	$m{value} = '';

	if    ($cmd eq '1') { $mes .= 'ここは$1ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '2') { $mes .= 'ここは$10ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '3') { $mes .= 'ここは$100ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '4') { $mes .= 'ここは$1000ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '5') {
		$mes .= 'ﾊｲﾛｳへようこそ!<br>';
		$mes .= '前のｶｰﾄﾞより大きいか小さいかを当てるｹﾞｰﾑです<br>';
		$mes .= '同じｶｰﾄﾞの場合は負けですので注意してくださいね<br>';
		$mes .= '一回10ｺｲﾝです<br>';
	}
	elsif ($cmd eq '6') { # ﾄﾞｯﾍﾟﾙ
		$mes .= 'ﾄﾞｯﾍﾟﾙへようこそ!<br>';
		$mes .= '3枚のｶｰﾄﾞの中から、ﾃﾞｨｰﾗｰが引いたｶｰﾄﾞと同じｶｰﾄﾞを引けば勝ちです<br>';
		$mes .= '一回10ｺｲﾝです<br>';
	}
	elsif ($cmd eq '7') { # ﾌﾞﾗｯｸｼﾞｬｯｸ
		$mes .= 'ﾌﾞﾗｯｸｼﾞｬｯｸへようこそ!<br>';
		$mes .= '21を超えずﾃﾞｨｰﾗｰより大きい数になれば勝ちです<br>';
		$mes .= '一回最大10000ｺｲﾝです<br>';
	}
	elsif ($cmd eq '8') { # ﾎﾟｰｶｰ
		$mes .= 'ﾎﾟｰｶｰへようこそ!<br>';
	}
#	elsif ($cmd eq '9') { # ﾋｯﾄｱﾝﾄﾞﾌﾞﾛｰ
#		$mes .= '今準備中だよ<br>';
#		$mes .= 'ごめんね<br>';
#	}
	elsif ($cmd eq '10') { # ﾊｲﾛｳ2
		$mes .= 'ﾊｲﾛｳ2へようこそ!<br>';
		$mes .= '前のｶｰﾄﾞより大きいか小さいかを当てるｹﾞｰﾑです<br>';
		$mes .= '同じｶｰﾄﾞはでません<br>';
		$mes .= '一回10ｺｲﾝです<br>';
	}
	elsif ($cmd eq '11') { # 裏ﾄﾞｯﾍﾟﾙ
		$mes .= '裏ﾄﾞｯﾍﾟﾙへようこそ!<br>';
		$mes .= 'ﾃﾞｨｰﾗｰに同じｶｰﾄﾞを当てられないようにするｹﾞｰﾑです<br>';
		$mes .= '一回100ｺｲﾝです<br>';
	}
	elsif ($cmd eq '12') { # ﾎﾟｰｶｰ
		$mes .= 'ﾛｲﾔﾙﾎﾟｰｶｰへようこそ!<br>';
	}
	else {
		&refresh;
		&n_menu;
	}
}


#=================================================
# ｽﾛｯﾄ
#=================================================
sub tp_100 { &_slot(1) }
sub tp_200 { &_slot(10) }
sub tp_300 { &_slot(100) }
sub tp_400 { &_slot(1000) }
sub _slot {
	my $bet = shift;
	
	if ($cmd eq '0') {
		if ($m{coin} >= $bet) {
			my @m = ('∞','♪','†','★','７');
			my @o = (5,10, 15,  20,  30,  50); # ｵｯｽﾞ 一番左はﾁｪﾘｰが2つそろいのとき
			my @s = ();
			$s[$_] = int(rand(@m)) for (0 .. 2);
			$mes .= "[\$$betｽﾛｯﾄ]<br>";
			$mes .= "<p>【$m[$s[0]]】【$m[$s[1]]】【$m[$s[2]]】</p>";
			$m{coin} -= $bet;
			
			if ($s[0] == $s[1]) { # 1つ目と2つ目
				if ($s[1] == $s[2]) { # 2つ目と3つ目
					my $v = $bet * $o[$s[0]+1]; # +1 = ﾁｪﾘｰ2そろい
					$m{coin} += $v;
					$mes .= "なんと!! $m[$s[0]] が3つそろいました!!<br>";
					$mes .= 'おめでとうございます!!<br>';
					$mes .= "***** ｺｲﾝ $v 枚 GET !! *****<br>";
					&c_up('cas_c');
					&use_pet('casino');
					&casino_win_common;
				}
				elsif ($s[0] == 0) { # ﾁｪﾘｰのみ1つ目と2つ目がそろえばよい
					my $v = $bet * $o[0];
					$m{coin} += $v;
					$mes .= 'ﾁｪﾘｰが2つそろいました♪<br>';
					$mes .= "ｺｲﾝ $v 枚Up♪<br>";
					&c_up('cas_c');
					&use_pet('casino');
					&casino_win_common;
				}
				else {
					$mes .= '<p>ﾊｽﾞﾚ</p>';
					$m{act} += 1;
				}
			}
			else {
				$mes .= '<p>ﾊｽﾞﾚ</p>';
				$m{act} += 1;
			}
			$mes .= 'もう一度やりますか?';
			&menu('Play!', 'やめる');
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	else {
		&begin;
	}
}

#=================================================
# ﾊｲﾛｳ
#=================================================
sub tp_500 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "【$m[$m{value}]】<br>次のｶｰﾄﾞは High? or Low?";
			&menu('High!(高い)','Low!(低い)');
			
			$m{tp} = 510;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました!<br>";
		&send_twitter("$m{name}がﾊｲﾛｳでｺｲﾝを $m{stock} 枚当てました") if $m{stock} > 150000;
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_510 {
	if ($cmd eq '') {
		my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
		$mes .= "【$m[$m{value}]】<br>次のｶｰﾄﾞは High? or Low?";
		&menu('High!(高い)','Low!(低い)');

		return;
	}

	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
	
	$m{value} = int(rand(@m));
	$mes .= "【$m[$stock_old]】-> 【$m[$m{value}]】<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # 高い選択で高い時
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # 低い選択で低い時
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= 'おめでとうございます!<br>';
			$mes .= "$m{stock}ｺｲﾝ Get!<br>";
			$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
			&menu('挑戦する','やめる');

			&c_up('cas_c');
			&use_pet('casino');
			&run_tutorial_quest('tutorial_highlow_1');
	}
	else { # 負け
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 6;
		&run_tutorial_quest('tutorial_highlow_1');
	}
	$m{tp} = 500;
}


#=================================================
# ﾄﾞｯﾍﾟﾙ
#=================================================
sub tp_600 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('★','◆','▲');
			$m{value} = int(rand(@m));
			$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$m{value}]】<br>";
			$mes .= '<p>【□】【□】【□】</p><p>どのｶｰﾄﾞを選びますか?</p>';
	
			&menu('左','真ん中','右');
			$m{tp} = 610;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_610 {
	my @m = ('★','◆','▲');
	my @s = (0,1,2);
	my $a = int(rand(@m));
	
	$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$m{value}]】<br>";
	$mes .= "<p>【$m[$s[$a]]】【$m[$s[$a-1]]】【$m[$s[$a-2]]】</p>";
	
	if (   ($cmd eq '0' && $m[$m{value}] eq $m[$s[$a]])       # 左選択
		|| ($cmd eq '1' && $m[$m{value}] eq $m[$s[$a-1]])     # 真ん中選択
		|| ($cmd eq '2' && $m[$m{value}] eq $m[$s[$a-2]]) ) { # 右選択
		
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 6;
			$mes .= 'おめでとうございます!<br>';
			$mes .= "ｺｲﾝ $m{stock} 枚 Get!<br>";
			$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
			&menu('挑戦する','やめる');
			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # 負け
		$m{coin} -= 10;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 5;
	}
	$m{tp} = 600;
}

#=================================================
# ﾌﾞﾗｯｸｼﾞｬｯｸ　未実装：ｲﾝｼｭﾗﾝｽ
#=================================================

sub h_to_v {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 14;
		$i++;
	}
	return $v;
}
sub v_to_h {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 14) - 1;
		$v -= $v % 14;
		$v /= 14;
		$i++;
	}
	return @h;
}

sub sph_to_v {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 25;
		$i++;
	}
	return $v;
}
sub spv_to_h {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 25) - 1;
		$v -= $v % 25;
		$v /= 25;
		$i++;
	}
	return @h;
}
#=================================================
# 手札処理
#=================================================
sub tp_700 {
	if($cmd eq '0') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		if ($m{coin} > 0){
			$mes .= $m{stock} ? qq|ﾍﾞｯﾄ<input type="text" name="bet_money" value="$m{stock}" class="text_box1" style="text-align:right">枚<br>|:
				qq|ﾍﾞｯﾄ<input type="text" name="bet_money" value="10" class="text_box1" style="text-align:right">枚<br>|;
		}
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="賭ける" class="button1"></p></form>|;
		$m{tp} = 705;
	}
	else{
	&begin;
	}
}

sub tp_705{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @handicap_p = (0,0,0,1,2,3,4,5,6,7,8,9,10,11,12);
	my @handicap_d = (0,1,2,3,3,3,4,4,4,5,5,5,6,7,8,9,10,11,12);
	my $n = 1;
	my @h = ();
	if($in{bet_money} > 0 && $in{bet_money} !~ /[^0-9]/){
		$m{stock} = $in{bet_money} > 10000 ? 10000:$in{bet_money};

		if ($m{coin} >= $m{stock}) {
			$h[0] = $handicap_d[int(rand(@handicap_d))];
			$h[1] = $handicap_p[int(rand(@handicap_p))];
			$h[2] = int(rand(@m));
			$mes .= "ｺｲﾝ $m{stock} 枚賭けました<br>";
			$mes .= "ﾃﾞｨｰﾗｰのｱｯﾌﾟｶｰﾄﾞ【$m[$h[0]]】<br>";
			$m{value} = &h_to_v(@h);
			$mes .= "【 ";
			until($h[$n] eq ''){
				$mes .= "$m[$h[$n]] ";
				$n++;
			}
			$mes .= "】<br>どうする?";
			$m{tp} = 710;
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			push(@amenus,'Split(分ける)') if($m{coin} >= $m{stock} * 2 && $h[1] == $h[2]);
			&menu(@amenus);
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	else {
		&begin;
	}
}

sub tp_710{&draw;}

sub draw{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my $pcount = 0;
	my $ace = 0; #A処理
	my $n = 0; #ﾌﾟﾚｲﾔｰの枚数
	my @h = &v_to_h($m{value});

	$mes .= "ﾃﾞｨｰﾗｰのｱｯﾌﾟｶｰﾄﾞ【$m[$h[0]]】<br>";

	if($cmd eq '0') {
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";

		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$m{coin} -= $m{stock};
			$m{value} = '';
			$mes .= '<p>ﾊﾞｰｽﾄです。もう一度やりますか?</p>';
			&menu('Play!','やめる');
			$m{act} += 6;
			$m{tp} = 700;
		}else {
			$mes .= "どうする?";
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 710;
		}
	}
	elsif($cmd eq '1'){
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";
		$mes .= '<p>この手で勝負</p>';
		$m{tp} = 720;
		&n_menu;
	}
	elsif($cmd eq '2'){
		$m{coin} -= $m{stock} / 2;
		$m{act} += 6;
		$m{value} = '';
		$mes .= '<p>降りました。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{tp} = 700;
	}
	elsif($cmd eq '3'){
		$m{stock} *= 2;
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";

		$m{tp} = 720;
		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$m{coin} -= $m{stock};
			$m{value} = '';
			$mes .= '<p>ﾊﾞｰｽﾄです。もう一度やりますか?</p>';
			&menu('Play!','やめる');
			$m{act} += 6;
			$m{tp} = 700;
		}else{
			&n_menu;
		}
	}elsif($cmd eq '4' && @h == 3) {
		$m{stock} *= 2;
		$mes .= "Splitしました";
		$h[2] = int(rand(@m));
		$mes .= "【$m[$h[1]] $m[$h[2]]】<br>";
		if($h[1] != 0){
			$mes .= "【$m[$h[1]] 】<br>";
			$m{value} = &h_to_v(@h);
			$m{tp} = 750;
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
		}else {
			$mes .= "【$m[$h[1]]】<br>";
			$m{value} = &h_to_v(@h);
			$m{tp} = 765;
			&n_menu;
		}
	}else {
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";
		$mes .= "どうする?";
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		push(@amenus,'Split(分ける)') if($m{coin} >= $m{stock} * 2 && $h[1] == $h[2]);
		&menu(@amenus);
		$m{tp} = 710;
	}
}


sub tp_720{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my $pcount = 0;
	my $dcount = 0;
	my $cards = 1; #ﾃﾞｨｰﾗｰの枚数
	my $bj = 1; #賭け金及びﾌﾞﾗｯｸｼﾞｬｯｸ処理
	my $ace = 0; #A処理
	my $n = 0; #ﾌﾟﾚｲﾔｰの枚数
	my @h = ();
	my $ran = 0;

	#standﾃﾞｨｰﾗｰの手決定,勝利判定
	$ace = 0;
	@h = &v_to_h($m{value});
	$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$h[0]] ";
	if($h[0] == 0){
		$ace++;
		$dcount += 11;
	}
	elsif ($h[0] > 9){
		$dcount += 10;
	}
	else {
		$dcount += $h[0] + 1;
	}
	until($dcount > 16){ #17以上になるまで引く
		$ran = int(rand(@m));
		$mes .= "$m[$ran] ";
		if($ran == 0){
			$ace++;
			$dcount += 11;
		}
		elsif ($ran > 9){
			$dcount += 10;
		}
		else {
			$dcount += $ran + 1;
		}
		while($dcount > 21 && $ace > 0) {
			$dcount -= 10;
			$ace--;
		}

		$cards++;
	}
	$mes .= "】<br>";

	$n = 1;
	$ace = 0;
	until($h[$n] eq ''){
		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}
		$n++;
	}
	while($pcount > 21 && $ace > 0) {
		$pcount -= 10;
		$ace--;
	}

	$bj += 2 if $pcount == 21 && $n == 3;
	$bj += 3 if $dcount == 21 && $cards == 2;

	if($bj == 1){ #どちらもﾌﾞﾗｯｸｼﾞｬｯｸでないとき
		$mes .= "ﾌﾟﾚｲﾔｰ【$pcount】 ﾃﾞｨｰﾗｰ【$dcount】<br>";
	}
	elsif($bj == 3){ #ﾌﾟﾚｲﾔｰのみﾌﾞﾗｯｸｼﾞｬｯｸの時
		$mes .= "ﾌﾟﾚｲﾔｰ【Blackjack】<br>";
	}
	elsif($bj == 4){ #ﾃﾞｨｰﾗｰがﾌﾞﾗｯｸｼﾞｬｯｸの時
		$mes .= "ﾃﾞｨｰﾗｰ【Blackjack】<br>";
	}
	else { #どちらもﾌﾞﾗｯｸｼﾞｬｯｸの時
		$mes .= "ﾌﾟﾚｲﾔｰ【Blackjack】 ﾃﾞｨｰﾗｰ【Blackjack】<br>";
	}


	if ($dcount > 21 || $bj == 3 || $pcount > $dcount){ #勝ち
		$m{stock} *= $bj;
		$m{value} = '';
		$m{coin} += $m{stock};
		$mes .= 'おめでとうございます!<br>';
		$mes .= "$m{stock}ｺｲﾝ Get!<br>";
		$mes .= '<p>もう一度やりますか?</p>';
		&menu('挑戦する','やめる');
		&c_up('cas_c');
		&use_pet('casino');
		&casino_win_common;
	}
	elsif(($pcount == $dcount && $bj != 4)) {
		$m{value} = '';
		$mes .= '<p>もう一度やりますか?</p>';
		&menu('Play!','やめる');
	}
	else { # 負け
		$m{coin} -= $m{stock};
		$m{value} = '';
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 4;
	}
	$m{tp} = 700;
}

sub tp_750{&split;}#Split専用分岐

sub split {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my $pcount = 0;
	my $ace = 0; #A処理
	my $n = 0; #ﾌﾟﾚｲﾔｰの枚数
	my @h = &v_to_h($m{value});

	$mes .= "ﾃﾞｨｰﾗｰのｱｯﾌﾟｶｰﾄﾞ【$m[$h[0]]】<br>";

	if($cmd eq '0') {
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】<br>";

		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$mes .= '<p>ﾊﾞｰｽﾄです。</p>';
			@h = ($h[0],23,$h[1],int(rand(@m)));
			$mes .= "【$m[$h[2]] $m[$h[3]]】<br>";
			$m{value} = &sph_to_v(@h);
			$m{tp} = 760;
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
		}else {
			$mes .= "【$m[$h[1]] 】<br>";
			$mes .= "どうする?";
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 750;
		}
	}
	elsif($cmd eq '1'){
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】<br>";
		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$pcount++ if $n == 3 && $pcount == 21;
		$mes .= '<p>second hand</p>';
		@h = ($h[0],$pcount,$h[1],int(rand(@m)));
		$mes .= "【$m[$h[2]] $m[$h[3]]】<br>";
		$m{value} = &sph_to_v(@h);
		$m{tp} = 760;
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	}
	elsif($cmd eq '2'){
		$mes .= '<p>降りました。</p>';
		@h = ($h[0],0,$h[1],int(rand(@m)));
		$mes .= "【$m[$h[2]] $m[$h[3]]】<br>";
		$m{value} = &sph_to_v(@h);
		$m{act} += 6;
		$m{tp} = 760;
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	}
	elsif($cmd eq '3'){
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";

		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$pcount = 23;
			$mes .= '<p>ﾊﾞｰｽﾄです。</p>';
		}
		@h = ($h[0],$pcount,0,$h[1],int(rand(@m)));
		$mes .= "【$m[$h[3]] $m[$h[4]]】<br>";
		$m{value} = &sph_to_v(@h);
		$m{tp} = 760;
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	} else {
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";
		$mes .= "どうする?";
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
		$m{tp} = 750;
	}
}

sub tp_760 {&split_2;}

sub split_2 {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my $pcount = 0;
	my $ace = 0; #A処理
	my $n = 0; #ﾌﾟﾚｲﾔｰの枚数
	my $nsub;
	my @h = &spv_to_h($m{value});

	$mes .= "ﾃﾞｨｰﾗｰのｱｯﾌﾟｶｰﾄﾞ【$m[$h[0]]】<br>";

	if($cmd eq '0') {
		$n = 2;
		$n++ if $h[$n] == 0;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ
		$m{value} = &sph_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 2;
		$n++ if $h[$n] == 0;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";
		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$mes .= '<p>ﾊﾞｰｽﾄです。</p>';
			@h = $h[2] == 0 ? ($h[0],$h[1],0,23):($h[0],$h[1],23);
			$m{value} = &sph_to_v(@h);
			$m{tp} = 770;
			&n_menu;
		}else {
			$mes .= "どうする?";
			my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
			push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 760;
		}
	}
	elsif($cmd eq '1'){
		$n = 2;
		$n++ if $h[$n] == 0;
		$nsub = $n;
		$mes .= "【";
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】<br>";
		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$pcount++ if $n - $nsub == 2 && $pcount == 21;
		@h = $h[2] == 0 ? ($h[0],$h[1],0,$pcount):($h[0],$h[1],$pcount);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	}
	elsif($cmd eq '2'){
		$mes .= '<p>降りました。</p>';
		@h = $h[2] == 0 ? ($h[0],$h[1],0,0):($h[0],$h[1],0);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	}
	elsif($cmd eq '3'){
		$n = 2;
		$n++ if $h[$n] == 0;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #新しく引いたｶｰﾄﾞ

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 2;
		$n++ if $h[$n] == 0;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";

		if($pcount > 21){ # ﾊﾞｰｽﾄ
			$mes .= '<p>ﾊﾞｰｽﾄです。</p>';
			$pcount = 23;
		}

		@h = $h[2] == 0 ? ($h[0],$h[1],0,$pcount,0):($h[0],$h[1],$pcount,0);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	} else {
		$n = 1;
		$mes .= "【";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "】";
		$mes .= "どうする?";
		my @amenus = ('hit(もう一枚)!','stand(勝負)!','Surrender(降りる)');
		push(@amenus,'Double down(最後の一枚)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
		$m{tp} = 760;
	}
}

sub tp_765 {#Ace Split専用
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @h = &v_to_h($m{value});

	if($h[2] > 8){
		$h[1] = 22;
	}else {
		$h[1] = 12 + $h[2];
	}

	@h = ($h[0],$h[1],0,int(rand(@m)));
	$mes .= "ﾃﾞｨｰﾗｰのｱｯﾌﾟｶｰﾄﾞ【$m[$h[0]]】<br>";
	$mes .= "【$m[$h[2]] $m[$h[3]]】<br>";
	if($h[3] > 8){
		$h[2] = 22;
	}else {
		$h[2] = 12 + $h[3];
	}
	@h = ($h[0],$h[1],$h[2]);
	$m{value} = &sph_to_v(@h);
	$m{tp} = 770;
	&n_menu();
}

sub tp_770 {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my $pcount = 0;
	my $dcount = 0;
	my $cards = 1; #ﾃﾞｨｰﾗｰの枚数
	my $bj = 1; #賭け金及びﾌﾞﾗｯｸｼﾞｬｯｸ処理
	my $ace = 0; #A処理
	my $n; #ﾌﾟﾚｲﾔｰの枚数
	my $nsub;
	my @h = ();
	my $ran = 0;
	my $is_dd = 0;
	my $is_dd2 = 0;
	my $pwin = 0;
	my $get_coin = 0;

	#standﾃﾞｨｰﾗｰの手決定,勝利判定
	$ace = 0;
	@h = &spv_to_h($m{value});
	$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$h[0]] ";
	if($h[0] == 0){
		$ace++;
		$dcount += 11;
	}
	elsif ($h[0] > 9){
		$dcount += 10;
	}
	else {
		$dcount += $h[0] + 1;
	}
	until($dcount > 16){ #17以上になるまで引く
		$ran = int(rand(@m));
		$mes .= "$m[$ran] ";
		if($ran == 0){
			$ace++;
			$dcount += 11;
		}
		elsif ($ran > 9){
			$dcount += 10;
		}
		else {
			$dcount += $ran + 1;
		}
		while($dcount > 21 && $ace > 0) {
			$dcount -= 10;
			$ace--;
		}

		$cards++;
	}
	$mes .= "】<br>";
	$dcount = 23 if $dcount > 21;
	$h[0] = $dcount;

	$h[0]++ if $h[0] == 21 && $cards == 2;

	$mes .= "ﾃﾞｨｰﾗｰ【";
	$mes .= $h[0] > 22 ? "ﾊﾞｰｽﾄ":
	$h[0] == 22 ? "Blackjack":
	$h[0];
	$mes .= "】<br>";
	$mes .= "ﾌﾟﾚｲﾔｰ【";
	$mes .= $h[1] > 22 ? "ﾊﾞｰｽﾄ":
	$h[1] == 22 ? "Blackjack":
	$h[1] == 0 ? "Surrender":
	$h[1];
	$mes .= "】<br>";
	$is_dd++ if($h[2] == 0 && $h[3] ne '');
	$is_dd2++ if(($h[3] ne '' && $h[3] == 0 && $is_dd == 0)||($h[4] == 0 && $is_dd == 1));
	my $second_hand = $is_dd == 1 ? $h[3]:$h[2];
	$mes .= "ﾌﾟﾚｲﾔｰ【";
	$mes .= $second_hand > 22 ? "ﾊﾞｰｽﾄ":
	$second_hand == 22 ? "Blackjack":
	$second_hand == 0 ? "Surrender":
	$second_hand;
	$mes .= "】<br>";

	$get_coin = $m{coin};

	if($h[0] == 22) {
		if($h[1] == 22){
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
			if ($h[1] == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
		if($second_hand == 22){
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
			if ($second_hand == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
	}
	else {
		if ($h[1] == 23){
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
		}
		elsif ($h[1] > 0 && ($h[0] > 22 || $h[1] == 22 || $h[0] < $h[1])){ #勝ち
			$m{coin} += $m{stock} / 2;
			$m{coin} += $m{stock} / 2 if $is_dd == 1;
			$m{coin} += $m{stock} if $h[1] == 22;
			$pwin++;
		}
		elsif($h[0] == $h[1]) {
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
			if ($h[1] == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
		if ($second_hand > 22){
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
		}
		elsif ($second_hand > 0 && ($h[0] > 22 || $second_hand == 22 || $h[0] < $second_hand)){ #勝ち
			$m{coin} += $m{stock} / 2;
			$m{coin} += $m{stock} / 2 if $is_dd2 == 1;
			$m{coin} += $m{stock} if $second_hand == 22;
			$pwin++;
		}
		elsif($h[0] == $second_hand) {
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
			if ($second_hand == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
	}
	$get_coin = $m{coin} - $get_coin;
	if ($pwin > 0 && $get_coin >= 0){ #勝ち
		$m{value} = '';
		$mes .= 'おめでとうございます!<br>';
		$mes .= "$get_coinｺｲﾝ Get!<br>";
		$mes .= '<p>もう一度やりますか?</p>';
		&menu('挑戦する','やめる');
		&c_up('cas_c') for (1..$pwin);
		&use_pet('casino') for (1..$pwin);
		&casino_win_common;
	}
	else { # 負け
		$m{value} = '';
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 6;
	}
	$m{tp} = 700;
}

#=================================================
# Jacks or Better
#=================================================
sub h_to_vj {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 53;
		$i++;
	}
	return $v;
}
sub v_to_hj {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 53) - 1;
		$v -= $v % 53;
		$v /= 53;
		$i++;
	}
	return @h;
}

#=================================================
# 手札処理
#=================================================
sub tp_800 {
	if ($cmd eq '0'){
		$mes .= "どの台でプレイしますか？<br>";
		&menu("やめる","1プレイ10ｺｲﾝ","1プレイ100ｺｲﾝ","1プレイ1000ｺｲﾝ");
		$m{tp} += 10;
	}
	else {
		&begin;
	}
}

sub tp_810 {
	my @bet_money = (10,100,1000);
	if($cmd eq '1' || $cmd eq '2' || $cmd eq '3'){
		$mes .= "1プレイ$bet_money[$cmd-1]ｺｲﾝの台で遊びます<br>";
		$m{tp} += $cmd;
		&menu("Go","やめる");
	}else {
		&begin;
	}
}

sub tp_811 {&deal_first(10);}

sub tp_821{&change_card();}

sub tp_831{&deal_second(10);}

sub tp_812 {&deal_first(100);}

sub tp_822{&change_card();}

sub tp_832{&deal_second(100);}

sub tp_813 {&deal_first(1000);}

sub tp_823{&change_card();}

sub tp_833{&deal_second(1000);}

sub deal_first{
	my $need_money = shift;
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = ();

	if ($cmd eq '0') {
		if ($m{coin} >= $need_money) {
			my $ran = $m{cas_c} > 50000 ? 1000:6000 - ($m{cas_c} / 10);
			$m{stock} = int(rand($ran));
			@h = &draw_new(@h);

			$m{value} = &h_to_vj(@h);
			$mes .= "【 ";
			for my $i (0..4){
				$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
			}
			$mes .= "】<br>";
			$mes .= "交換するカードを選んでね";
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="checkbox" name="change_0" value="1">1枚目($suit[$h[0] / 13] $num[$h[0] % 13])を交換<br>|;
			$mes .= qq|<input type="checkbox" name="change_1" value="1">2枚目($suit[$h[1] / 13] $num[$h[1] % 13])を交換<br>|;
			$mes .= qq|<input type="checkbox" name="change_2" value="1">3枚目($suit[$h[2] / 13] $num[$h[2] % 13])を交換<br>|;
			$mes .= qq|<input type="checkbox" name="change_3" value="1">4枚目($suit[$h[3] / 13] $num[$h[3] % 13])を交換<br>|;
			$mes .= qq|<input type="checkbox" name="change_4" value="1">5枚目($suit[$h[4] / 13] $num[$h[4] % 13])を交換<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="交換" class="button1"></p></form>|;

			$m{tp} += 10;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	else {
		&begin;
	} 
}

sub draw_new{
	my $c;
	my $j;
	my @h;
	$j = 0;
	until($_[$j] eq ''){
		$h[$j] = $_[$j];
		$j++;
	}
	for my $i (0..4){
		next if $h[$i] ne '';
		while(1){
			$c = int(rand(52));
			my $go = 1;
			for $j(0..$i-1){
				$go = 0 if $h[$j] == $c;
			}
			last if $go == 1;
		}
		$h[$i] = $c;
	}
	if($m{stock} == 1){
		@h = (12,10,9,11,0);
	}
	if($m{stock} == 2){
		@h = (25,13,22,24,23);
	}
	if($m{stock} == 3){
		@h = (26,38,35,37,36);
	}
	if($m{stock} == 4){
		@h = (48,51,39,50,49);
	}
	if($m{stock} == 5){
		@h = (1,10,9,11,0);
	}
	if($m{stock} == 6){
		@h = (25,0,22,24,23);
	}
	if($m{stock} == 7){
		@h = (26,38,34,37,36);
	}
	if($m{stock} == 8){
		@h = (48,26,39,50,49);
	}
	$m{stock} = 0;
	$j = 1;
	while(1){
		last if $h[$j] eq '';
		if($h[$j-1] > $h[$j]){
			my $tem = $h[$j-1];
			$h[$j-1] = $h[$j];
			$h[$j] = $tem;
			$j = 1;
			next;
		}
		$j++;
	}

	return @h;
}

sub change_card{
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @sub_h = &v_to_hj($m{value});
	my @h = ();
	my $i;

	for my $j (0..4){
		next if $in{"change_$j"};
		push @h, $sub_h[$j];
	}
	$m{value} = &h_to_vj(@h);

	$i = 0;
	$mes .= "【 ";
	until($h[$i] eq '') {
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
		$i++;
	}
	$mes .= "】<br>";
	$m{tp} += 10;
	&n_menu;
}

sub deal_second{
	my $need_money = shift;
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = &v_to_hj($m{value});

	@h = &draw_new(@h);
	$mes .= "【 ";
	for my $i (0..4){
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
	}
	$mes .= "】<br>";
	$m{value} = &h_to_vj(@h);

	&check_hand();

	if($m{stock} == 1000){
		$mes .= "Royal Straight Flash<br>";
	}elsif($m{stock} == 200){
		$mes .= "Straight Flash<br>";
	}elsif($m{stock} == 25){
		$mes .= "Four of a kind<br>";
	}elsif($m{stock} == 10){
		$mes .= "Full House<br>";
	}elsif($m{stock} == 7){
		$mes .= "Flash<br>";
	}elsif($m{stock} == 5){
		$mes .= "Straight<br>";
	}elsif($m{stock} == 4){
		$mes .= "Three of a kind<br>";
	}elsif($m{stock} == 3){
		$mes .= "Two pair<br>";
	}elsif($m{stock} == 1){
		$mes .= "Jack or Better<br>";
	}else{
		$mes .= "No pair<br>";
	}

	if ($m{stock} > 0) { 
		$m{stock} *= $need_money;
		$mes .= 'おめでとうございます!<br>';
		$mes .= "ｺｲﾝ $m{stock} 枚 Get!<br>";
		$m{coin} += $m{stock};
		$m{stock} = $m{value} = 0;
		&menu('play','やめる');
		&c_up('cas_c');
		&use_pet('casino');
		&casino_win_common;
	}
	else { # 負け
		$m{coin} -= $need_money;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 5;
	}
	$m{tp} -= 20;
}

sub check_hand{
	my @h = &v_to_hj($m{value});
	my $is_straight = 0;
	my $is_royal = 0;
	my $is_flash = 0;
	my $is_four = 0;
	my $is_three = 0;
	my $pair_num = 0;
	my $pair_high = 0;
	my @subh = ();
	my @suith = ();
	my $i;

	for $i (0..4){
		$subh[$i] = $h[$i] % 13;
		$suith[$i] = ($h[$i] - $subh[$i]) / 13;
	}
	$i = 1;
	while(1){
		last if $subh[$i] eq '';
		if($subh[$i-1] > $subh[$i]){
			my $tem = $subh[$i-1];
			$subh[$i-1] = $subh[$i];
			$subh[$i] = $tem;
			$i = 1;
			next;
		}
		$i++;
	}
	if($subh[0]+1 == $subh[1]&& $subh[0]+2 == $subh[2] && $subh[0]+3 == $subh[3] && $subh[0]+4 == $subh[4]){
		$is_straight = 1;
	}
	if($subh[0] == 0 && $subh[1] == 9 && $subh[2] == 10 && $subh[3] == 11 && $subh[4] == 12){
		$is_royal = 1;
		$is_straight = 1;
	}
	if($suith[0] == $suith[1] && $suith[0] == $suith[2] && $suith[0] == $suith[3] && $suith[0] == $suith[4]){
		$is_flash = 1;
	}
	for $i (0..12){
		my $card = 0;
		for my $j (0..4){
			$card++ if $subh[$j] == $i;
		}
		if($card == 4){
			$is_four = 1;
		}elsif($card == 3){
			$is_three = 1;
		}elsif($card == 2){
			$pair_num++;
			$pair_high = $i;
		}
	}

	if($is_royal && $is_straight && $is_flash){
		$m{stock} = 1000;
	}elsif($is_straight && $is_flash){
		$m{stock} = 200;
	}elsif($is_four){
		$m{stock} = 25;
	}elsif($is_three && $pair_num == 1){
		$m{stock} = 10;
	}elsif($is_flash){
		$m{stock} = 7;
	}elsif($is_straight){
		$m{stock} = 5;
	}elsif($is_three){
		$m{stock} = 4;
	}elsif($pair_num == 2){
		$m{stock} = 3;
	}elsif($pair_num == 1 && ($pair_high > 9 || $pair_high == 0)){
		$m{stock} = 1;
	}else{
		$m{stock} = 0;
	}
}

#=================================================
# hit and blow(廃止)
#=================================================
sub tp_900 {
	&begin;
}

#=================================================
# ﾊｲﾛｳ2
#=================================================
sub tp_1000 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "【$m[$m{value}]】<br>次のｶｰﾄﾞは High? or Low?";
			&menu('High!(高い)','Low!(低い)');
			
			$m{tp} = 1010;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました!<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_1010 {
	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
	my @n;
	push @n, int(rand($#m - $stock_old)) + $stock_old+1 unless $stock_old == $#m;
	push @n, int(rand($stock_old)) unless $stock_old == 0;
	
	$m{value} = $n[int(rand(@n))];
	$mes .= "【$m[$stock_old]】-> 【$m[$m{value}]】<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # 高い選択で高い時
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # 低い選択で低い時
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= 'おめでとうございます!<br>';
			$mes .= "$m{stock}ｺｲﾝ Get!<br>";
			$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
			&menu('挑戦する','やめる');

			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # 負け
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 6;
	}
	$m{tp} = 1000;
}

#=================================================
# 裏ﾄﾞｯﾍﾟﾙ
#=================================================
sub tp_1100 {
	if ($cmd eq '0') {
		if ($m{coin} >= 100) {
			my @m = ('★','◆','▲','●');
			$m{value} = int(rand(@m));
			$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【□】<br>";
			$mes .= '<p>【★】【◆】【▲】【●】</p><p>どのｶｰﾄﾞを選びますか?</p>';
	
			&menu('★','◆','▲','●');
			$m{tp} = 1110;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_1110 {
	my @m = ('★','◆','▲','●');
	my $a = int(rand(@m));
	
	$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$a]】<br>";
	$mes .= "貴方のｶｰﾄﾞ【$m[$cmd]】</p>";
	
	if ($cmd >= 0 && $cmd < @m && $cmd != $a) {
		$m{stock} = 100 if $m{stock} == 0;
		$m{stock} = int(1.5 * $m{stock});
		$mes .= 'おめでとうございます!<br>';
		$mes .= "ｺｲﾝ $m{stock} 枚 Get!<br>";
		$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
		&menu('挑戦する','やめる');
		&c_up('cas_c');
		&use_pet('casino');
	}
	else { # 負け
		$m{coin} -= 100;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 7;
	}
	$m{tp} = 1100;
}

#=================================================
# ﾛｲﾔﾙﾎﾟｰｶｰ
#=================================================
sub tp_1200 {
	if($cmd eq '0') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		if ($m{coin} > 0){
			$mes .= $m{stock} ? qq|ﾍﾞｯﾄ<input type="text" name="bet_money" value="$m{stock}" class="text_box1" style="text-align:right">枚<br>|:
				qq|ﾍﾞｯﾄ<input type="text" name="bet_money" value="10" class="text_box1" style="text-align:right">枚<br>|;
		}
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="賭ける" class="button1"></p></form>|;
		$m{tp} += 10;
	}
	else{
		&begin;
	}
}

sub tp_1210 {
	if($in{bet_money} > 0 && $in{bet_money} !~ /[^0-9]/){
		$m{stock} = $in{bet_money} > 500 ? 500:$in{bet_money};
		if ($m{coin} >= $m{stock}) {
			my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
			my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
			my @h = ();
			@h = &draw_r_card(@h);
			@h = &draw_r_card(@h);
			$m{value} = &h_to_vj(@h);
			$mes .= "【 ";
			for my $i (0..1){
				$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
			}
			$mes .= "】<br>";
			$mes .= "次のｶｰﾄﾞを引く？	<br>";
			$m{tp} += 10;
			&menu('draw','double up','やめる');
		}
	}
	else {
		&begin;
	}
}

sub tp_1220 {
	if($cmd eq '2'){
		$m{coin} -= $m{stock};
		$m{stock} = $m{value} = 0;
		$mes .= '<p>もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 1;
		$m{tp} -= 20;
	
	}else{
		if($cmd eq '1' && $m{coin} > $m{stock}*2){
			$m{stock} *= 2;
		}
		my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
		my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
		my @h = &v_to_hj($m{value});
		@h = &draw_r_card(@h);
		$m{value} = &h_to_vj(@h);
		$mes .= "【 ";
		for my $i (0..$#h){
			$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
		}
		$mes .= "】<br>";
		if(@h < 5){
			$mes .= "次のｶｰﾄﾞを引く？	<br>";
			&menu('draw','double up','やめる');	
		}else {
			my $bet = $m{stock};
			my $base = $m{stock};
			&check_hand();
			
			if($m{stock} == 1000){
				$mes .= "Royal Straight Flash<br>";
				$bet *= 100;
			}elsif($m{stock} == 200){
				$mes .= "Straight Flash<br>";
				$bet *= 0;
			}elsif($m{stock} == 25){
				$mes .= "Four of a kind<br>";
				$bet *= 50;
			}elsif($m{stock} == 10){
				$mes .= "Full House<br>";
				$bet *= 10;
			}elsif($m{stock} == 7){
				$mes .= "Flash<br>";
				$bet *= 0;
			}elsif($m{stock} == 5){
				$mes .= "Straight<br>";
				$bet *= 5;
			}elsif($m{stock} == 4){
				$mes .= "Three of a kind<br>";
				$bet *= 1;
				$bet = int($bet);
			}elsif($m{stock} == 3){
				$mes .= "Two pair<br>";
				$bet *= 0;
			}elsif($m{stock} == 1){
				$mes .= "One pair<br>";
				$bet *= -1;
			}else{
				$mes .= "One pair<br>";
				$bet *= -1;
			}
			
			if ($bet >= 0) { 
				$mes .= 'おめでとうございます!<br>';
				$mes .= "ｺｲﾝ $bet 枚 Get!<br>";
				$m{coin} += $bet;
				$m{value} = 0;
				$m{stock} = $base;
				&menu('play','やめる');
				&c_up('cas_c');
				&use_pet('casino');
				&casino_win_common;
			}
			else { # 負け
				$m{coin} += $bet;
				$m{value} = 0;
				$m{stock} = $base;
				$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
				&menu('Play!','やめる');
				$m{act} += 8;
			}
			$m{tp} -= 20;
		}
	}
}

sub draw_r_card{
	my @r_cards = (0, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 35, 36, 37, 38, 39, 48, 49, 50, 51);
	my $c;
	my $j;
	my @h;
	$j = 0;
	until($_[$j] eq ''){
		$h[$j] = $_[$j];
		$j++;
	}
	while(1){
		$c = $r_cards[int(rand(@r_cards))];
		my $go = 1;
		for $i(0..$j-1){
			$go = 0 if $h[$i] == $c;
		}
		last if $go == 1;
	}
	$h[$j] = $c;

	$j = 1;
	while(1){
		last if $h[$j] eq '';
		if($h[$j-1] > $h[$j]){
			my $tem = $h[$j-1];
			$h[$j-1] = $h[$j];
			$h[$j] = $tem;
			$j = 1;
			next;
		}
		$j++;
	}

    return @h;
}


sub casino_win_common {
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('casino');
	}
}
1; # 削除不可
