sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
my $this_depot_file = "$userdir/$id/depot.cgi";
#=================================================
# �S�� Created by Merino
#=================================================

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{act} >= 100) {
		$mes .= "$m{name}�͏����x�����Ƃ邱�Ƃɂ���<br>���ɍs���ł���̂� $GWT����ł�";
		$m{act} = 0;
		&wait;
		return 0;
	}
	return 1;
}

#=================================================
# �S���ƭ�
#=================================================
sub tp_100 {
	if (-f "$userdir/$id/rescue_flag.cgi" # ڽ����׸ނ����邩
		|| $time < $w{reset_time} # �I�풆
		|| !defined $cs{name}[$y{country}]) { # ���폜

			unlink "$userdir/$id/rescue_flag.cgi" or &error("$userdir/$id/rescue_flag.cgi�폜���s") if -f "$userdir/$id/rescue_flag.cgi";
			$mes .= "���Ԃɋ~�o����܂���<br>";
			
			&refresh;
			&n_menu;
			&escape;
	}
	else {
		$mes .= "$m{name}��$c_y��$cs{prison_name}[$y{country}]�ɕ����߂��܂���<br>";
		$mes .= '�ǂ����܂���?<br>';
		&menu('������҂�','�E�������݂�','�Q�Ԃ�');
		$m{tp} += 10;
	}
}

sub tp_110 {
	# �E�o
	if ($cmd eq '1') {
		$mes .= "$m{name}�͒E�����ł��������F�X�Ǝ����Ă݂�<br>";
		if ( int(rand(4)) == 0 ) { # ����
			$mes .= '�Ȃ�Ƃ�$cs{prison_name}[$y{country}]����E�o���邱�Ƃɐ�������!<br>';
			$m{tp} += 10;
		}
		elsif ( $m{cha} > rand(1000)+400 ) {
			$mes .= '�Ŏ��U�f����$cs{prison_name}[$y{country}]����E�o���邱�Ƃɐ�������!<br>';
			$m{tp} += 10;
		}
		else {
			$mes .= '�ǂ���疳���Ȃ悤���c<br>';
			$m{act} += 10;
			$m{tp} = 100;
		}
		&n_menu;
	}
	# �Q�Ԃ�
	elsif ($cmd eq '2') {
		$mes .= "�Q�Ԃ�ƊK���Ƒ�\\���߲�Ă�������A�葱����$GWT��������܂�<br>";
		$mes .= "$c_m �𗠐؂�A$c_y�ɐQ�Ԃ�܂���?<br>";
		&menu('��߂�','�Q�Ԃ�');
		$m{tp} = 200;
	}
	else {
		$m{tp} = 100;
		&tp_100;
	}
}

#=================================================
# �S���E�o
#=================================================
sub tp_120 {
	$m{tp} += 10;
	$m{value} = int(rand(40))+40;
	$m{turn}  = int(rand(4)+4);
	$mes .= "$cs{prison_name}[$y{country}]����E�o���܂���! <br>";
	$mes .= "$c_y�E�o�܂Ŏc��y$m{turn}��݁z�G���̋C�z�y$m{value}%�z<br>";
	$mes .= '�ǂ���ɐi�݂܂���?<br>';
	&menu('��','�E');
	$m{value} += int( 10 - rand(21) ); # �}10
	$m{value} = int(rand(30)) if $m{value} < 10;
}

#=================================================
# ٰ���ƭ� �߂܂邩�E�o����܂�
#=================================================
sub loop_menu {
	$mes .= "$c_y�E�o�܂Ŏc��y$m{turn}��݁z�G���̋C�z�y$m{value}%�z<br>";
	$mes .= '�ǂ���ɐi�݂܂���?<br>';
	int(rand(3)) == 0 ? &menu('��','�E') : &menu('��','���i','�E');
}
sub tp_130 {
	# ������
	if ( $m{value} > rand(110)+30 ) {
		$mes .= '�G���Ɍ������Ă��܂���!!<br>';
		$m{tp} += 10;
		&n_menu;
	}
	# �E�o����
	elsif (--$m{turn} <= 0) {
		if ($m{country} && $y{country}) {
			&c_up('esc_c');
			&use_pet('escape');
			&write_yran('esc', 1, 1);
		}
		&mes_and_world_news("������$c_y����̎��͒E�o�ɐ������܂���!");
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('prison');
		}
		
		&refresh;
		&n_menu;
		&escape;
	}
	else {
		&loop_menu;
	}
	$m{value} += int( 10 - rand(21) ); # �}10
	$m{value} = int(rand(30)) if $m{value} < 10;
}
# ����������:�����؂�� or �߂܂�
sub tp_140 {
	if ( rand(6) < 1 ) {
		$mes .= '�Ȃ�Ƃ��G����U��؂�܂���<br>';
		$m{tp} -= 10;
		&loop_menu;
	}
	else {
		$mes .= '�G���Ɉ͂܂�$cs{prison_name}[$y{country}]�ւƘA��߂���܂���<br>';
		$m{tp} = 100;
		$m{act} += 20;
		&n_menu;
	}
}


#=================================================
# �Q�Ԃ�
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$mes .= "$e2j{ceo}�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
#		if ($m{name} eq $m{vote} || &is_daihyo) {
#			$mes .= "���̑�\\�҂�$e2j{ceo}�ɗ���₵�Ă���ꍇ�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
#			$m{tp} = 100;
#			&n_menu;
#		}
		elsif ($m{shogo} eq $shogos[1][0]) {
			$mes .= "$shogos[1][0]�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($cs{member}[$y{country}] >= $cs{capacity}[$y{country}]) {
			$mes .= "$c_y�͒���������ς��ł�<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5) {
			$mes .= "�����͐Q�Ԃ�܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($m{random_migrate} eq $w{year}) {
			$mes .= "�����͐Q�Ԃ�܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
		else {
			require './lib/move_player.cgi';
			&move_player($m{name}, $m{country}, $y{country});
			&escape;
			
			$m{shogo} = $shogos[1][0];

			$m{rank} -= $m{rank} > 10 ? 2 : 1;
			$m{rank} = 1 if $m{rank} < 1;
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "�K����$rank_name�ɂȂ�܂���<br>";
			if($m{super_rank}){
				$mes .= "������$m{rank_name}�͖��_�E�Ȃ̂Ŗ��̂͂��̂܂܂ł�<br>";
			}

			&mes_and_world_news("$cs{name}[$y{country}]�ɐQ�Ԃ�܂���", 1);
			$m{country} = $y{country};
			$m{vote} = '';
			
			# ��\�߲��Down
			for my $key (qw/war dom mil pro/) {
				$m{$key.'_c'} = int($m{$key.'_c'} * 0.4);
			}

			&refresh;
			&wait;
			&n_menu;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		$m{tp} = 100;
		&n_menu;
	}
}

#=================================================
# come by pet
#=================================================
sub tp_300 {
	if (int(rand(10)) + 10 <= $m{pet_c}) {
		$m{tp} = 320;
		&{'tp_' . $m{tp}};
		return;
	}
	$mes .= '�ǂ̍��̘S���֍s���܂���?<br>';
	&menu('������',@countries,'��߂�');
	$m{tp} = 310;
}

sub tp_310 {
	if($cmd eq '' || $cmd == $m{country} || $cmd == $w{country} + 1){
		&refresh;
		&n_menu;
	}else{
		$y{country} = $cmd;
		&add_prisoner;
	}
}

sub tp_320 {
	$mes .= '�o�J���X���߯Ă�A��čs���܂��B<br>';
	$layout = 2;
	my($count, $sub_mes) = &radio_my_pet_depot;

	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<p><input type="submit" value="���o��" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="���o��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_330 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $add_line = '';
		my @lines = ();
		open my $fh, "+< $this_depot_file" or &error("$this_depot_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			++$count;
			if (!$new_line && $cmd eq $count) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				if($kind eq '3') {
					$new_line = $line;
					if($m{pet}) {
						$add_line = "$kind<>$m{pet}<>$m{pet_c}<>0<>\n";
						$mes .= "$pets[$m{pet}][1]��$m{pet_c}��a��";
					}
				} else {
					$mes .= '�߯ĈȊO�͘A��Ă����܂���<br>';
					push @lines, $line;
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line) {
			push @lines, $add_line if $add_line;
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my $s_mes;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			if ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�����o���܂���<br>";
			}
		}
		else {
			close $fh;
		}
	}
	$mes .= '�ǂ̍��̘S���֍s���܂���?<br>';
	&menu('������',@countries,'��߂�');
	$m{tp} = 310;
}

sub radio_my_pet_depot {
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script">|;
	$sub_mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	open my $fh, "< $this_depot_file" or &error("$this_depot_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		next if ($kind ne '3');
		$sub_mes .= qq|<input type="radio" name="cmd" value="$count">|;
		$sub_mes .= qq|[��]$pets[$item_no][1]��$item_c$lock_mes<br>|;
	}
	close $fh;
	
	return $count, $sub_mes;
}
#=================================================
# �S��̧�ق��玩���̖��O������
#=================================================
sub escape {
	if (-f "$logdir/$y{country}/prisoner.cgi") {
		my @lines = ();
		open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name,$country,$flag) = split /<>/, $line;
			push @lines, $line unless $name eq $m{name};
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}


1; # �폜�s��
