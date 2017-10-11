require './lib/move_player.cgi';
#=================================================
# �d�� Created by Merino
#=================================================

# �S������
$GWT *= 2;

# �d������̂ɕK�v������
my $need_lv = 1;

# �d������̂ɕK�v�ȋ��z
my $need_money = $m{sedai} > 100 ? $rank_sols[$m{rank}]+300000 : $rank_sols[$m{rank}]+$m{sedai}*3000;

# ���E����Í��̏ꍇ�ANPC���֎d������̂ɕK�v�ȋ��z
my $need_money_npc = 1000000;

# �K���d���̐_�l�~�Պm��(���̈�)
my $random_god_par = 30;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͎d�����邱�Ƃ��ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{lv} < $need_lv) {
		$mes .= "�d������ɂ� $need_lv ���وȏ�K�v�ł�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{random_migrate} eq $w{year} && !$config_test) {
		$mes .= "���N�����ς��͈ڐЂł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{tp} = 1 if $m{tp} > 1;

	if ($m{country}) {
		$mes .= "�d������葱���Ƃ���$GWT��������܂�<br>";
		$mes .= "���̍��Ɏd������Ƒ�\\���߲�ĂƊK����������܂�<br>";
		$mes .= "�������Ɏd������ꍇ�͊K����������܂���<br>" if $union;
		$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����K�v������܂�<br>";
		
		# �Í�
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]�Ɏd������ꍇ�́A���̔N�ɂȂ�܂ő��̍��Ɏd�����邱�Ƃ͂ł��܂���<br>|;
			$mes .= qq|$cs{name}[$w{country}]�Ɏd������ꍇ�́A��\\�߲�Ă� 0 �ɂȂ�A$need_money_npc G�x�����K�v������܂�<br></font>|;
		}
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		&menu('��߂�', @countries, '���Q����');
	}
	else {
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]�Ɏd������ꍇ�́A���̔N�ɂȂ�܂ő��̍��Ɏd�����邱�Ƃ͂ł��܂���<br>|;
			$mes .= qq|$cs{name}[$w{country}]�Ɏd������ꍇ�́A��\\�߲�Ă� 0 �ɂȂ�A$need_money_npc G�x�����K�v������܂�<br></font>|;
		}
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		&menu('��߂�', @countries, '�K��');
	}
}

sub tp_1 {
	return if &is_ng_cmd(1 .. $w{country}+1);

	$m{tp} = 200;
	&{ 'tp_'.$m{tp} };
}

sub tp_200 {
	return if (&is_ng_cmd(1 .. $w{country}+1));

	if($cmd <= $w{country}){ # �d��
		if ($m{country}) { return unless &is_move_from_country; } # �����獑�֎d���ł��邩�ǂ���
		else { return unless &is_move_from_neverland; } # ����݂��獑�֎d���ł��邩�ǂ���

		if ($w{world} >= $#world_states-3 && $w{world} < $#world_states) {
			# �����E�g���E�O���u��������݂���d�����鎞�ɍ���ٰٕ\���łǂ��̍��ɍs���̂�������
			# �܂�Aٰق����ķ�ݾق���Ύ����s���������ɍs���Ă��܂�
			$mes .= "�{���Ɏd�����܂����H";
		}
		else {
			my $line = &get_countries_mes($cmd);
			my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
			$mes .= $country_rule;
			$mes .= "�{����$cs{name}[$cmd]�Ɏd�����܂����H";
		}

		&menu('��߂�','�d��');
	}
	else { # ���Q�E�K���d��
		if ($m{country}) {
			return unless &is_move_from_country; # ��������Q�ł��邩�ǂ���
			$mes .= '�{���ɕ��Q���܂����H';
			&menu('��߂�','���Q');
		}
		else { # ��{�Ƃ��ēK���d���ɐ����͂Ȃ��̂� is_move_from_neverland �͗v��Ȃ�
			$mes .= '�{���ɓK���d�����܂����H';
			&menu('��߂�','�d��');
		}
	}
	$m{value} = $cmd;
	$m{tp} = 300;
}

sub tp_300 {
	return if &is_ng_cmd(1 .. $w{country}+1);

	$cmd = $m{value};

	if ($cmd == $w{country} + 1) {
		if ($m{country}) { &country_to_neverland; } # �������Q
		else { &neverland_to_random; } # ����݁��K���d��
	}
	elsif (defined $cs{name}[$cmd]) { # �������݂���
		if ($m{country}) { &country_to_country; } # �������̍�
		else { &neverland_to_country; } # ����݁���
	}
}

# ͯ�����
sub tp_100 {
	my @head_hunt;
	$mes .= '�ǂ̊��U���󂯂܂���?<br>';
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($hname, $hcountry) = split /<>/, $line;
		$mes .= "$hname���� $cs{name}[$hcountry] �ւ̊��U���󂯂Ă��܂�<br>";
		push @head_hunt, $cs{name}[$hcountry] if defined($cs{name}[$hcountry]);
	}
	close $fh;
	$m{tp} += 10;
	&menu('�f��', @head_hunt);
}

sub tp_110 {
	unless (defined($cmd)) { # $cmd ����`
		$m{tp} -= 10;
		&{ 'tp_'.$m{tp} };
		return;
	}
	elsif ($cmd eq '0') { # �f��
		$mes .= "���U��f�邱�Ƃɂ��܂���<br>";
		open my $fh, "> $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
		close $fh;
		&refresh;
		&n_menu;
		return;
	}

	my $i_c = 0;
	my ($from_name, $from_country);
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$i_c;
		if($i_c == $cmd){
			my($hname, $hcountry) = split /<>/, $line;
			if ($hcountry eq $m{country}) { # ��������̊��U������݌��ʏ���
				$mes .= "�����Ɏd���͂ł��܂���<br>";
				&begin; # �m�F���ĂȂ����� begin �ŗǂ��̂�����
			}
			elsif (defined $cs{name}[$hcountry]) { # �������݂���
				if ($m{country}) {
					if ($m{name} eq $cs{ceo}[$m{country}]) { # �N��Ȃ�����݌��ʎ���
						$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
						&refresh;
						&n_menu;
						close $fh;
						return;
					}
					$cs{money}[$m{country}] += $need_money;
				}
				($from_name, $from_country) = ($hname, $hcountry);
			}
			else { # ����ݏ���
				&begin; # �m�F���ĂȂ����� begin �ŗǂ��̂�����
			}
			last;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;

	if (defined($from_name) && defined($from_country)) {
		&move_player($m{name}, $m{country}, $from_country);
		$m{country} = $from_country;
		$m{vote} = '';
		&mes_and_world_news("$from_name�̗U����$cs{name}[$from_country]�Ɏd�����܂���",1);
	}

	&refresh;
	&n_menu;
}

#=================================================
# ��������Q
#=================================================
sub country_to_neverland {
	return unless &is_move_from_country;

	&move_player($m{name}, $m{country}, 0);
	$m{country} = 0;
	$m{rank} = 0;
	$m{rank_exp} = 0;
	$m{vote} = '';

	&mes_and_world_news("$c_m���痧��������Q�̗��ɏo�܂���",1);

	# ��\�߲��0
	for my $k (qw/war dom mil pro/) {
		$m{$k.'_c'} = 0;
	}

	$mes .= "���ɍs���ł���̂�$GWT����ł�<br>";
	&refresh;
	&wait;
}

#=================================================
# ����݂���K���d��
#=================================================
sub neverland_to_random {
	if ($w{world} eq $#world_states) { # �Í�
		$cmd = int(rand($w{country} - 1) + 1);
	}
	else { # �Í�����Ȃ�
		$cmd = int(rand($w{country}) + 1);
	}
	return unless &is_move_from_neverland;

	$m{random_migrate} = $w{year};
	&n_menu;

	&mes_and_world_news("�K����$cs{name}[$cmd]�Ɏd�����܂���",1);
	if (rand($random_god_par) < 1) {
		require './lib/shopping_offertory_box.cgi';
		&get_god_item(5);
	}
	&move_to_country;
}

#=================================================
# �����獑�֎d��
#=================================================
sub country_to_country {
	return unless &is_move_from_country;
	# �Í�
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country}) {
			$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
			&begin;
			return;
		}
		elsif ($cmd eq $w{country}) {
			require './lib/vs_npc.cgi';
			if ($need_money_npc > $m{money}) {
				$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
				&begin;
				return;
			}
			elsif (!&is_move_npc_country) {
				&begin;
				return;
			}
			$need_money = $need_money_npc;
		}
	}

	$m{money} -= $need_money;
	$cs{money}[$m{country}] += $need_money;
	$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";

	unless ($union eq $cmd) {
		$m{rank} -= $m{rank} > 10 ? 2 : 1;
		$m{rank} = 1 if $m{rank} < 1;
		my $rank_name = &get_rank_name($m{rank}, $m{name});
		$mes .= "�K����$rank_name�ɂȂ�܂���<br>";

		# ��\�߲�Ĕ���
		for my $k (qw/war dom mil pro/) {
			$m{$k.'_c'} = int($m{$k.'_c'} * 0.5);
		}
	}

	$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
	&wait;

	&mes_and_world_news("$cs{name}[$cmd]�Ɏd�����܂���",1) unless $w{world} eq $#world_states;
	&move_to_country;
}

#=================================================
# ����݂��獑�֎d��
#=================================================
sub neverland_to_country {
	return unless &is_move_from_neverland;
	# �Í�
	if ($w{world} eq $#world_states) {
		if ($cmd eq $w{country}) {
			require './lib/vs_npc.cgi';
			if ($need_money_npc > $m{money}) {
				$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
				&begin;
				return;
			}
			elsif (!&is_move_npc_country) {
				&begin;
				return;
			}
			$need_money = $need_money_npc;
			$m{money} -= $need_money;
			$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";
			$m{rank} = 1 if $m{rank} < 1;
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "�K����$rank_name�ɂȂ�܂���<br>";
			$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
			&wait;
		}
	}

	&n_menu;

	&mes_and_world_news("$cs{name}[$cmd]�Ɏd�����܂���",1) unless $w{world} eq $#world_states;
	&move_to_country;
}

#=================================================
# ���֎d������ۂ̒��ۓI�֐�
#=================================================
sub move_to_country {
	&move_player($m{name}, $m{country}, $cmd);
	$m{rank} = 1 if $m{rank} < 1;
	$m{next_salary} = $time + 3600 * $salary_hour;
	$m{country} = $cmd;
	$m{vote} = '';
	&refresh;
}

#=================================================
# ������d���ł��邩 �ł��� 1 �ł��Ȃ� 0
#=================================================
sub is_move_from_country {
	# �����d��
	if ($cmd eq $m{country}) {
		$mes .= "�����Ɏd���͂ł��܂���<br>";
	}
	# ���
	elsif ($cmd <= $w{country} && $cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]�͒���������ς��ł�<br>";
	}
	# �N��
	elsif ($m{name} eq $cs{ceo}[$m{country}]) {
		$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
	}
	# ������
	elsif ($m{name} eq $m{vote}) {
		$mes .= "$c_m��$e2j{ceo}�̗��������C����K�v������܂�<br>";
	}
	# �����E�g���E�O���u�E�ّ�
	elsif($w{world} eq $#world_states-1 || $w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5){
		$mes .= $cmd == ($w{country} + 1) ? "���𗣂�邱�Ƃ͂ł��܂���<br>" : "���𗠐؂邱�Ƃ͂ł��܂���<br>";
	}
	elsif ($need_money > $m{money} && ($cmd < $w{country} + 1) ) {
		$mes .= "�ڐЂ���ɂ� $need_money G�K�v�ł�<br>";
	}
	else {
		return 1;
	}
	&begin;
	return;
}

#=================================================
# ����݂���d���ł��邩 �ł��� 1 �ł��Ȃ� 0
# �d���ł���ꍇ�ɂ� $cmd �ɓK���ȍs���悪�����Ă���
#=================================================
sub is_move_from_neverland {
	if ($w{world} eq $#world_states-1) { # ����
		$cmd = int(rand($w{country}) + 1);
	}
	elsif ($w{world} eq $#world_states-2) { # �g��
		$cmd = $w{country} - int(rand(2));
	}
	elsif ($w{world} eq $#world_states-3) { # �O���u
		$cmd = $w{country} - int(rand(3));
	}
	# �K���d������Ȃ���Β�������ɂ�����
	elsif ($m{value} < $m{country}+1 && $cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]�͒���������ς��ł�<br>";
		&begin;
		return;
	}

	return 1;
}

1; # �폜�s��
