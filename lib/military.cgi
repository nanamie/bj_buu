#=================================================
# �R�� Created by Merino
#=================================================

$gik_limit = 10; # �U�v�̏��

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= '�I����Ԓ��͐푈�ƌR���͂ł��܂���<br>';
		if ($m{value} eq 'military_ambush'){
			open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgi̧�ق��J���܂���");
			eval { flock $fh, 2; };
			seek  $fh, 0, 0;
			truncate $fh, 0;
			close $fh;
		}
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ����s���܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= '�R�����s���܂�<br>�ǂ���s���܂���?<br>';
	}
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		&menu('��߂�','�H�������D','������D��','���m����]','������@','�U�v','�U��','�҂�����','�H�������D(����)','������D��(����)','���m����](����)');
	}else{
		&menu('��߂�','�H�������D','������D��','���m����]','������@','�U�v','�U��','�҂�����');
	}
}
sub tp_1 {
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		return if &is_ng_cmd(1..10);
	}else{
		return if &is_ng_cmd(1..7);
	}
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '7') {
		$mes .= "�G������̌R���s�ׂ�����������A�G������̐i�R��҂��������Ċh�������܂�($GWT���`)<br>";
		$mes .= "�ǂ���̑҂����������܂���?<br>";
		&menu('��߂�', '�R���s�ׂ�������', '�i�R��҂�����');
	}
	else { # 1-6 8-10
		if    ($cmd eq '1')  { $mes .= "���荑�ɔE�э��ݐH����D���܂�<br>"; }
		elsif ($cmd eq '2')  { $mes .= "���荑�̎���ٰĂ��h���������𗬏o�����܂�<br>"; }
		elsif ($cmd eq '3')  { $mes .= "���荑�̕��m����]���A�����̕��m�ɂ��܂�<br>"; }
		elsif ($cmd eq '4')  { $mes .= "���荑�̓����̏�Ԃ�F�����ɍs���܂�<br>"; }
		elsif ($cmd eq '5')  { $mes .= "���荑�Ɉ����\\�𗬂��F�D�x�������܂�<br>"; }
		elsif ($cmd eq '6')  { $mes .= "���荑�̏�ǂ�j�󂵁A�h��͂������܂�<br>"; }
		elsif ($cmd eq '8')  { $mes .= "���荑�ɔE�э��ݑ�ڂɐH����D���܂�<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '9')  { $mes .= "���荑�̎���ٰĂ��h������ڂɂ����𗬏o�����܂�<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '10') { $mes .= "���荑�̕��m���ڂɐ��]���A�����̕��m�ɂ��܂�<br>"; $GWT *= 2.5; }
		$mes .= "�ǂ̍��Ɍ������܂���?($GWT��)<br>";
		&menu('��߂�', @countries);
	}
}

#=================================================
# �҂�����
#=================================================
sub tp_700 {
	require './lib/_rampart.cgi'; # ���
	if ($cmd eq '1') {
		$mes .= "�G������̌R���s�ׂ��Ȃ������������񂵊Ď����܂�<br>";
		$mes .= "�҂������̗L�����Ԃ͍ō���$max_ambush_hour���Ԃ܂łł�<br>";
		$mes .= "���ɍs���ł���̂�$GWT����ł�<br>";
		$m{tp} += 10;
		$m{value} = 'military_ambush';
		
		# �푈�Ɠ����d�g�݂ł��������ǁA����̽ð�����K�v�Ȃ��̂ƁA̧�ٵ���݂P��ł��ނ̂ŁB
		open my $fh, ">> $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgi̧�ق��J���܂���");
		print $fh "$time<>$m{name}<>\n";
		close $fh;

		&before_action('icon_pet_exp', $GWT);
		&gain_mil_barrier(1);
		&wait;
	}
	elsif ($cmd eq '2') {
		$mes .= "�G������̐i�R��҂��������܂�<br>";
		$mes .= "�҂������̗L�����Ԃ͍ō���$max_ambush_hour���Ԃł�<br>";
		$mes .= "���ɍs���ł���̂�$GWT����ł�<br>";
		$m{value} = 'ambush';
		$m{tp} += 10;

		&before_action('icon_pet_exp', $GWT);
		&gain_mil_barrier(1);
		&wait;
	}
	else {
		&begin;
	}
}
sub tp_710 {
	$m{turn} = 1;
	$mes .= "�҂��������I�����܂���<br>";
	
	# �҂������ɂЂ�����������
	if (-s "$userdir/$id/ambush.cgi") {
		open my $fh, "+< $userdir/$id/ambush.cgi" or &error("$userdir/$id/ambush.cgi�t�@�C�����ǂݍ��߂܂���");
		eval { flock $fh, 2 };
		my $line = <$fh>;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		
		my @lines = split /<>/, $line;
		
		$mes .= join ",<br>", @lines;
		$mes .= "<br>��҂������Ō��ނ��܂���!<br>";
		$m{turn} = @lines;
	}

	# �R���҂������̎��A����t�@�C�����玩������������
	if ($m{value} ne 'ambush') {
		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($pat_time,$name) = split /<>/, $line;
			next if $name eq $m{name};
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		&run_tutorial_quest('tutorial_mil_ambush_1');
	}elsif (-s "$userdir/$id/war.cgi") {
		open my $fh, "+< $userdir/$id/war.cgi" or &error("$userdir/$id/war.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $result) = split /<>/, $line;
			
			if ($result eq '0') {
				$mes .= "$name�����ނ��܂���<br>";
			}
			elsif ($result eq '1') {
				$mes .= "$name�ɔs�k���܂���<br>";
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
=pod
		unless (&gain_mil_barrier(chomp($head_line))) {
			my($name, $result) = split /<>/, $head_line;
			if ($result eq '0') {
				$mes .= "$name�����ނ��܂���<br>";
			}
			elsif ($result eq '1') {
				$mes .= "$name�ɔs�k���܂���<br>";
			}
		}
=cut
	}

	&special_money($m{turn} * 500);
	&c_up('mat_c') for 1 .. $m{turn};
	&military_master_c_up('mat_c');
	&use_pet('mat') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '32');

	require './lib/_rampart.cgi'; # ���
	&gain_mil_barrier(0);

	&tp_1100;
}

#=================================================
# �R�����
#=================================================
sub tp_100 { &exe1("�H�������D����") }
sub tp_200 { &exe1("����ٰĂ��h������") }
sub tp_300 { &exe1("���m����]����") }
sub tp_400 { &exe1("��������@����") }
sub tp_500 { &exe1("�U�v������") }
sub tp_600 { &exe1('�U�������') }
sub tp_800 { &exe1("�H�����ڂɋ��D����") }
sub tp_900 { &exe1("����ٰĂ��ڂɊh������") }
sub tp_1000 { &exe1("���m���ڂɐ��]����") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});
	
	if ($m{country} eq $cmd) {
		$mes .= '�����͑I�ׂ܂���<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '�������͑I�ׂ܂���<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '�ŖS���Ă��鍑�͑I�ׂ܂���<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;

		# ���E��u�����v
		if (($w{world} eq '15' || ($w{world} eq '19' && $w{world_sub} eq '15'))) {
			$y{country} = int(rand($w{country}))+1;
			if ($cs{is_die}[&get_most_strong_country]){
				my $loop = 0;
				while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
					if($loop > 30) {
						$y{country} = &get_most_strong_country;
					}
					$y{country} = int(rand($w{country}))+1;
					$loop++;
				}
			}else {
				$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
			}
		}

		$GWT *= 2.5 if $m{tp} >= 810 && $m{tp} <= 1010;
		$mes .= "$_[0]$cs{name}[$y{country}]�Ɍ������܂���<br>";
		$mes .= "$GWT����ɓ�������\\��ł�<br>";

		$m{renzoku_c} = $y{country} eq $m{renzoku} ? $m{renzoku_c} + 1 : 1;
		$m{renzoku} = $y{country};

		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
}

#=================================================
# �R������
#=================================================
sub tp_110 { &form1('�H����D��') }
sub tp_210 { &form1('������s��') }
sub tp_310 { &form1('���]���s��') }
sub tp_410 { &form1('���T��') }
sub tp_510 { &form1('�����\\�𗬂�') }
sub tp_610 { &form1('�U����s��') }
sub tp_810 { &form1('�H����D��(����)') }
sub tp_910 { &form1('������s��(����)') }
sub tp_1010 { &form1('���]���s��(����)') }
sub form1 {
	$mes .= "$c_y�ɓ������܂���<br>";

	$m{tp} += 10;
	$m{value} = int(rand(20))+5;#$config_test ? 0 : int(rand(20))+5;
	$m{value} += int(rand(10)+1);#$config_test ? 0 : int(rand(10)+1); # �Q�[���o�����X���l���ď����l�ް�Ă͂��̂܂�
	$m{value} += 30 if $y{country} && ($pets[$m{pet}][2] ne 'no_ambush' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && &is_patrol($_[0]);
	if ($m{pet} == -1) { # հڲ�̖��ߍ��ݏ���
		$m{pet_c}--;
		if ($m{pet_c} <= 0) {
			$m{pet} = 0;
			$m{pet_c} = 0;
		}
	}

	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "�G���̋C�z�y $m{value}% �z<br>";
	$mes .= '�ǂ����܂���?<br>';
	&menu($_[0],'����������');
#	$m{value} += int(rand(10)+1); merino �̏����Y��H
}

#=================================================
# ٰ�ߺ���� ���s���邩��߂Ȃ����葱��(tp�Œ�)
#=================================================
sub loop_menu {
	$mes .= "�G���̋C�z�y $m{value}% �z<br>";
	$mes .= '�ǂ����܂���?';
	&menu('������', '��߂�');
}
sub tp_120 { &exe2 }
sub tp_220 { &exe2 }
sub tp_320 { &exe2 }
sub tp_420 { &exe2 }
sub tp_520 { &exe2 }
sub tp_620 { &exe2 }
sub tp_820 { &exe2 }
sub tp_920 { &exe2 }
sub tp_1020 { &exe2 }
sub exe2 {
	if ($cmd eq '0') { # ���s
		if ( $m{value} > rand(110)+35 ) { # ���s �P����rand(100)�ɂ����30%���炢�Ō������Ă��܂��̂� rand(110)+30�ɕύX
			$mes .= "�G���Ɍ������Ă��܂���!!<br>";
			$m{tp} = 1900;
			&n_menu;
		}
		else { # ����
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			if($m{tp} == 420 && $m{turn} < 7){
				my $tei_sp = rand($m{tei_c} / 500);
				$m{value} += $tei_sp > 5 ? int(rand(5)+1): int(rand(10-$tei_sp)+1);
			} else {
				$m{value} += int( $m{unit} eq '17' ? (rand(10)+1)*(0.7+rand(0.3)) : rand(10)+1 ); # �B���͏㏸�C�z�l0�`8�H �ʏ핔����1�`10
			}
			&loop_menu;
			$m{tp} -= 10;
		}
	}
	elsif ($cmd eq '1') { # �ދp
		$mes .= '�����グ�邱�Ƃɂ��܂�<br>';
		if ($m{turn} <= 0) { # �������Ȃ��ň����グ
			&refresh;
			&n_menu;
		}
		elsif ($m{tp} eq '420') { # ������@
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
		}
		else {
			my $tmp_tp = $m{tp};
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 1100;
			if ($tmp_tp eq '120' || $tmp_tp eq '220' || $tmp_tp eq '320' ||
				$tmp_tp eq '820' || $tmp_tp eq '920' || $tmp_tp eq '1020') {
				&run_tutorial_quest('tutorial_mil_1');
			}
			&n_menu;
		}
	}
	else {
		&loop_menu;
	}
}

#=================================================
# ����
#=================================================
sub get_mil_success {
	my $v = int( ($m{"$_[0]_c"} + $m{$_[1]}) * $m{turn} * rand($_[3]) );
	$v  = int(rand(500)+$_[2]-500) if $v > $_[2];
	$v *= 2 if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
	$v *= 2 if $cs{extra}[$m{country}] eq '2' && $cs{extra_limit}[$m{country}] >= $time;
	$m{stock} += $v;
	return $v;
}
sub get_mil_message {
	if ($m{stock} > $cs{$_[0]}[$y{country}]) {
		$mes .= "$c_y��$_[3]";
		$m{stock} = $cs{$_[0]}[$y{country}];
	} else {
		$mes .= "$_[2]";
	}
	$mes .= "<br>[ �A��$m{turn}�񐬌� İ��$_[1] $m{stock} ]<br>";
}
sub tp_130 { # ���D����
	my $v = &get_mil_success('gou', 'at', 3000, 4);
	&get_mil_message('food', '���D', "$v�̐H�����D�ɐ������܂���!", "�H�����s���܂���!");
}
sub tp_230 { # ���񐬌�
	my $v = &get_mil_success('cho', 'mat', 3000, 4);
	&get_mil_message('money', '����', "$v�̎������o�ɐ������܂���!", "$e2j{money}���s���܂���!");
}
sub tp_330 { # ���]����
	my $v = &get_mil_success('sen', 'cha', 2500, 4);
	&get_mil_message('soldier', '���]', "$v�l�̕��m���]�ɐ������܂���!", "���m���������܂���!");
}
sub tp_430{ # ��@
	$mes .= $m{turn} eq '1' ? "$e2j{food}�̏�����ɓ���܂���!<br>"
		  : $m{turn} eq '2' ? "$e2j{money}�̏�����ɓ���܂���!<br>"
		  : $m{turn} eq '3' ? "$e2j{soldier}�̏�����ɓ���܂���!<br>"
		  : $m{turn} eq '4' ? "$e2j{tax}�̏�����ɓ���܂���!<br>"
		  : $m{turn} eq '5' ? "$e2j{state}�̏�����ɓ���܂���!<br>"
		  : $m{turn} eq '6' ? "$e2j{strong}�̏�����ɓ���܂���!<br>"
		  : $m{turn} >   7  ? "��c���̉�b�𕷂��܂���!<br>"
		  :                   "������ւƌ������Ă݂܂�<br>"
		  ;
}
sub tp_530{ # �U�v
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = $gik_limit if $v > $gik_limit;
	$mes .= "�R�̏��𗬂��̂ɐ������܂���!<br>[ �A��$m{turn}�񐬌� İ�ًU�v $v% ]<br>";
}
sub tp_630{ # �U��
	my $v = $m{turn} <= 1 ? 1:
	      	$m{kou_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{kou_c}) / 2900);
	$mes .= "��ǂ�j�󂷂�̂ɐ������܂���!<br>[ �A��$m{turn}�񐬌� İ�ٍU�� $v% ]<br>";
}
sub tp_830 { # ���D����
	my $v = &get_mil_success('gou', 'at', 4500, 6);
	&get_mil_message('food', '���D', "$v�̐H�����D�ɐ������܂���!", "�H�����s���܂���!");
}
sub tp_930 { # ���񐬌�
	my $v = &get_mil_success('cho', 'mat', 4500, 6);
	&get_mil_message('money', '����', "$v�̎������o�ɐ������܂���!", "$e2j{money}���s���܂���!");
}
sub tp_1030 { # ���]����
	my $v = &get_mil_success('sen', 'cha', 4000, 6);
	&get_mil_message('soldier', '���]', "$v�l�̕��m���]�ɐ������܂���!", "���m���������܂���!");
}

#=================================================
# �����グ
#=================================================
sub tp_140 { # ���D
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_y�Ɋ�P�U�������{�B$v�̕��Ƃ����D���邱�Ƃɐ������܂���");
}
sub tp_240 { # ����
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_y�̎������BٰĂ��h�����A$v��$e2j{money}�𗬏o�����邱�Ƃɐ������܂���");
}
sub tp_340 { # ���]
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_y��$v�̕�����]���邱�Ƃɐ���!$c_m�̕��Ɏ�荞�݂܂���");
}
sub tp_840 { # ���D
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_y�Ɋ�P�U�������{�B$v�̕��Ƃ����D���邱�Ƃɐ������܂���");
}
sub tp_940 { # ����
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_y�̎������BٰĂ��h�����A$v��$e2j{money}�𗬏o�����邱�Ƃɐ������܂���");
}
sub tp_1040 { # ���]
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_y��$v�̕�����]���邱�Ƃɐ���!$c_m�̕��Ɏ�荞�݂܂���");
}
sub exe3 {
	my $k = shift;
	my $l = shift;

	&c_up("${l}_c") for 1 .. $m{turn};
	&military_master_c_up("${l}_c");
	$m{stock} = &use_pet($l, $m{stock}) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '33');
	$m{stock} = &seed_bonus($l, $m{stock});

	# ��m�͒D�R����1.1�{
	$m{stock} = int($m{stock} * 1.1) if  $cs{mil}[$m{country}] eq $m{name};
	# �N��͒D�R����1.05�{�A�\�N���Ȃ��1.2�{
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$m{stock} = int($m{stock} * $ceo_value);
	}
#	$m{stock} = int($m{stock} * 1.05) if  $cs{ceo}[$m{country}] eq $m{name};
	$m{stock} = int($m{stock} * 1.1) if  $m{unit} eq '17';
	$m{stock} = int($m{stock} * 0.3) if  $m{unit} eq '18';
	
	# �e���ݒ�
	$m{stock} = int($m{stock} * &get_modify('mil'));
	# �b��
	$m{stock} = &seed_bonus('red_moon', $m{stock});
	
	my $v = $m{stock} > $cs{$k}[$y{country}] ? int($cs{$k}[$y{country}]) : int($m{stock});
	$cs{$k}[$y{country}] -= $v;
	$cs{$k}[$m{country}] += $v;
	
	&write_cs;

	&special_money(int($v * 0.1));
	&write_yran($l, $v, 0,
					"${l}_t", $v, 1) if $v > 0;
	return $v;
}

# ----------------------------
sub tp_440 { # ��@
	my $bbs_name = $cs{bbs_name}[$y{country}] eq '' ? "$cs{name}[$y{country}]����c��" : $cs{bbs_name}[$y{country}];
	$mes .= "�y$c_y�̏��z$bbs_name<br>";
	$mes .= "$e2j{food}�F$cs{food}[$y{country}] <br>"       if $m{turn} >= 1;
	$mes .= "$e2j{money}�F$cs{money}[$y{country}] <br>"     if $m{turn} >= 2;
	$mes .= "$e2j{soldier}�F$cs{soldier}[$y{country}] <br>" if $m{turn} >= 3;
	$mes .= "$e2j{tax}�F$cs{tax}[$y{country}]% <br>"        if $m{turn} >= 4;
	$mes .= "$e2j{state}�F$country_states[ $cs{state}[$y{country}] ]<br>" if $m{turn} >= 5;
	$mes .= "$e2j{strong}�F$cs{strong}[$y{country}] <br>"   if $m{turn} >= 6;
	$mes .= "��ǁF$cs{barrier}[$y{country}]% <br>"             if $m{turn} >= 7;
	$mes .= "��L�̏���$c_m�̉�c���ɕ񍐂��܂���?<br>";
	&menu('��߂�','�񍐂���');
	$m{tp} += 10;
}	
sub tp_450 {
	my $bbs_name = $cs{bbs_name}[$y{country}] eq '' ? "$cs{name}[$y{country}]����c��" : $cs{bbs_name}[$y{country}];

	&c_up('tei_c') for 1 .. $m{turn};
	&military_master_c_up('tei_c');
	&use_pet('tei') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '36');
	&special_money($m{turn} * 500);

	my $lcomment = "$bbs_name<br>";
	my $need_count = 7;
	if ($m{turn} > $need_count) {
		$m{turn} += $m{turn} - $need_count if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
		&write_yran('tei', $m{turn}-$need_count, 1);
		$mes .= "$c_y�̉�c���i$bbs_name�j�̏������������ݕ����ł���<br>";
		
		my $count = $need_count;
		my @bbs_logs = ();
		open my $fh, "< $logdir/$y{country}/bbs.cgi" or &error("BBS���O���ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
			$mes .= "$bcomment<br>";
			$lcomment .= "$bcomment<br>";
			last if ++$count > $m{turn};
		}
		close $fh;
	}

	# BBS�ɒǋL
	if ($cmd eq '1') {
		my $w_name = $m{name};
		$w_name = '������' if $w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16');
		my $comment = "�y$c_y�z";
		$comment .= "$e2j{food}�F$cs{food}[$y{country}]/"       if $m{turn} >= 1;
		$comment .= "$e2j{money}�F$cs{money}[$y{country}]/"     if $m{turn} >= 2;
		$comment .= "$e2j{soldier}�F$cs{soldier}[$y{country}]/" if $m{turn} >= 3;
		$comment .= "$e2j{tax}�F$cs{tax}[$y{country}]%/"        if $m{turn} >= 4;
		$comment .= "$e2j{state}�F$country_states[ $cs{state}[$y{country}] ]/" if $m{turn} >= 5;
		$comment .= "$e2j{strong}�F$cs{strong}[$y{country}]/"   if $m{turn} >= 6;
		$comment .= "��ǁF$cs{barrier}[$y{country}]%/"         if $m{turn} >= 7;
		$comment .= "<br>$bbs_name�̉�b�𗧂��������܂���"     if $m{turn} > 7;

		my $comment2 = '';
		$comment2 .= $lcomment if $m{turn} > $need_count;

		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/bbs.cgi" or &error("$logdir/$m{country}/bbs.cgi ̧�ق��J���܂���");
		eval { flock $fh, 2; };
		push @lines, $_ while <$fh>;
		pop @lines if @lines > 50;
		unshift @lines, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment<>$m{icon}<>$m{icon_pet}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if($comment2){
			unless (-f "$logdir/$m{country}/bbs_log_$y{country}.cgi") {
				open my $fh2, "> $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi ̧�ق��J���܂���");
				close $fh2;
			}
			
			my @lines2 = ();
			open my $fh2, "+< $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi ̧�ق��J���܂���");
			eval { flock $fh2, 2; };
			push @lines2, $_ while <$fh2>;
			if(@lines2 > 50){
				pop @lines2;
			}
			unshift @lines2, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment2<>$m{icon}<>\n";
			seek  $fh2, 0, 0;
			truncate $fh2, 0;
			print $fh2 @lines2;
			close $fh2;
		}

		$mes .= "$c_m�̉�c���ɕ񍐂��܂���<br>";
	}
	else {
		$mes .= "$m{name}�̋��̓��ɔ�߂Ă������Ƃɂ��܂���<br>";
	}

	$m{tp} = 1100;
	&n_menu;
}

# ----------------------------
sub tp_540 { # �U�v
	&c_up('gik_c') for 1 .. $m{turn};
	&military_master_c_up('gik_c');
	&use_pet('gik') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '37');
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = $gik_limit if $v > $gik_limit;
	$v = &seed_bonus('gik', $v);
	&write_yran('gik', $v, 1) if $v > 0;
	for my $i (1 .. $w{country}) {
		next if $y{country} eq $i;
		
		my $u  = &union($y{country}, $i);
		$w{"f_$u"} -= $v;
		
		if ($w{"f_$u"} < rand(10)) {
			if ($w{"p_$u"} eq '1' && $w{world} ne '6') {
				$w{"p_$u"} = 0;
				&mes_and_world_news("<b>�U�v�ɂ��$c_y��$cs{name}[$i]�Ƃ̓��������􂳂��܂���</b>");
				require './lib/shopping_offertory_box.cgi';
				&get_god_item(1);
				if ($w{world} eq $#world_states-4) {
					require './lib/fate.cgi';
					&super_attack('breakdown');
				}
			}
			
			$w{"f_$u"} = int(rand(10));
		}
	}
	
	&special_money($m{turn} * 500);
	$mes .= "$c_y�Ƒ����̗F�D�x��$v%������̂ɐ������܂���<br>";
	$m{tp} = 1100;

	&run_tutorial_quest('tutorial_gikei_1');

	&n_menu;
	&write_cs;
}

# ----------------------------
sub tp_640 { # �U��
	&c_up('kou_c') for 1 .. $m{turn};
	&military_master_c_up('kou_c');
#	&use_pet('kou') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '37'); # 37 ����
	my $v = $m{turn} <= 1 ? 1:
	      	$m{kou_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{kou_c}) / 2900);
	$v *= 1.3 if  $cs{mil}[$m{country}] eq $m{name};
	$v = &seed_bonus('kou', $v);
	$v = int($v);
	&write_yran('kou', $v, 1) if $v > 0;

	# ��ǃf�[�^�}
	require './lib/_rampart.cgi'; # ���
	&change_barrier($y{country}, -$v);

	&special_money($m{turn} * 500);
	$mes .= "$c_y�̏�ǂ�$v%�j�󂷂�̂ɐ������܂���<br>";
	$m{tp} = 1100;

	&n_menu;
	&write_cs;
}

#=================================================
# ���s
#=================================================
sub tp_1900 {
	$m{act} += $m{turn};

	# �A���œ��������ƍ��m��������
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( (($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2 || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		&write_world_news("$c_m��$m{name}���R���C���Ɏ��s��$c_y��$cs{prison_name}[$y{country}]�ɗH����܂���");
		&add_prisoner;
	}
	else { # �ދp����
		$mes .= "�Ȃ�Ƃ��G����U��؂邱�Ƃ��ł��܂���<br>";
		&n_menu;
	}
	my $v = int( (rand(4)+1) );
	$m{exp} += $v;
	$m{rank_exp}-= int(rand(6)+5);
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	$mes .= "�C���Ɏ��s�������߁A$m{name}�ɑ΂���]����������܂���<br>";
}

#=================================================
# ����
#=================================================
sub tp_1100 {
	$m{act} += $m{turn};

	my $v = int( (rand(3)+3) * $m{turn} );
	$v = &use_pet('military', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '161');
	$m{exp} += $v;
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	$m{egg_c} += int(rand($m{turn})+$m{turn}) if $m{egg};

	if ($m{turn} >= 5) {
		$mes .= "�C���ɑ听��!$m{name}�ɑ΂���]�����傫���オ��܂���<br>";
		$m{rank_exp} += $m{turn} * 3;
	}
	else {
		$mes .= "�C���ɐ���!$m{name}�ɑ΂���]�����オ��܂���<br>";
		$m{rank_exp} += int($m{turn} * 1.5);
	}
	
	&daihyo_c_up('mil_c'); # ��\�n���x
	if ( $w{world} eq $#world_states) {
		require './lib/vs_npc.cgi';
#		if (rand(12) < $npc_mil || ($cs{strong}[$w{country}] < 50000 && rand(4) < $npc_mil) ){ # (1/12) + (1/4) - ( (1/12) * (1/4) ) = 0.3125
#		if (rand(14) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(5) < 1) ) { # (1/14) + (1/5) - ( (1/14) * (1/5) ) = 0.25714285714
		if (rand(13) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(4) < 1) ) { # (1/13) + (1/4) - ( (1/13) * (1/4) ) = 0.307692308
		   &npc_military;
		}
	}

	&after_success_action('military');

	&write_cs;
	&refresh;
	&n_menu;
}


#=================================================
# �R���҂������̌����肪����H
#=================================================
sub is_patrol {
	my $military_kind = shift;
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/patrol.cgi" or &error("$logdir/$y{country}/patrol.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pat_time,$name) = split /<>/, $line;
		next if $time > $pat_time + $max_ambush_hour * 3600;
		next if ++$sames{$name} > 1;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# �����l���ɑ΂��Ăǂꂭ�炢���񂵂Ă��邩
	my $p = $w{world} eq $#world_states && $y{country} eq $w{country} ? 80 : 30;
	if (@lines > 0 && (@lines / ($cs{member}[$y{country}]+1) * 100) >= rand($p) ) {
		my $a = @lines;
		my $line = $lines[rand(@lines)];
		my($pat_time,$name) = split /<>/, $line;
		&mes_and_world_news("$c_y�ɌR���s�ׂ����s�B���񂵂Ă���$name�̊Ď��̖ڂ�����܂���");
		
		my $yid = unpack 'H*', $name;
		if (-d "$userdir/$yid") {
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}$military_kind($date)<>";
			close $fh;
		}

		return 1;
	}
	return 0;
}

sub military_master_c_up {
	# �܂��������� +1 ����������4������ɂ���� +1
	if ($m{master_c} eq $_[0]) { &c_up($_[0]) for 0 .. (int($m{turn} / 4)); }
}

sub special_money {
	return unless $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');
	$m{money} += $_[0];
	$mes .= "���܂ł̌��т��F�߂�� $_[0] G�̌��J������������ꂽ<br>";
}

1; # �폜�s��
