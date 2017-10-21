require "$datadir/skill.cgi";
$is_battle = 1; # �����׸�1
#================================================
# �퓬 Created by Merino
#================================================

#Ⱥ�Ж��
#�@Ⱥ�Б���ɋZ���������Ƃ������̈ꕔ�̋Z��MP����Ȃ��Ō��ʂ����������
#�@�t�ɾ��ނȂǑ���ɓ����邱�Ƃ�O��Ƃ��Ȃ��Z�͌��ʂ��������Ȃ�
#�@��������Ⱥ�Д��������ȋC������
#�@���X�̖����܂߁A�U���׸ނ����p���Ă�̂����ɂ���

# ����ɂ��D��
my %tokkous = (
# '��������' => qr/�ア����/,
	'��' => qr/��/,
	'��' => qr/��/,
	'��' => qr/��/,
	'��' => qr/��|��/,
	'��' => qr/��|��/,
	'��' => qr/��|��/,
	'��' => qr/��|��|��/,
);

#================================================
# �g���l�� Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# ��ʕ\���⽷قŎg���̂Ÿ�۰��ٕϐ�
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$m_mdf= $m{mdf};
$y_df = $y{df};
$y_mdf= $y{mdf};
$m_ag = $m{ag};
$y_ag = $y{ag};

if    ($guas[$m{gua}][2] =~ /��|��|��|��/) { $m_df += $guas[$m{gua}][3]; }
elsif ($guas[$m{gua}][2] =~ /��|��|��/)    { $m_mdf+= $guas[$m{gua}][3]; }
if    ($guas[$y{gua}][2] =~ /��|��|��|��/) { $y_df += $guas[$y{gua}][3]; }
elsif ($guas[$y{gua}][2] =~ /��|��|��/)    { $y_mdf+= $guas[$y{gua}][3]; }
# �g�p����̂� AT or MAT, DF or MDF �̂ǂ��炩
if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y_mdf; }
if    ($weas[$y{wea}][2] =~ /��|��|��|��/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /��|��|��/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m_mdf; }

$m_ag -= $guas[$m{gua}][5];
$m_ag -= $weas[$m{wea}][5] if $guas[$m{gua}][0] ne '7';
$m_ag = int(rand(5)) if $m_ag < 1;

$y_ag -= $guas[$y{gua}][5];
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea}, $y{wea})) {
		$m_at = int(1.5 * $m_at);
		$y_at = int(0.75 * $y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}
# ����Ɩh��̑����ݒ�(�U����)
# �f��vs�h��� 0.3�{ �f��vs�h��Ȃ� 1.0�{
# ����vs�h��Ȃ� 1.0�{ ����vs�h����Ⴂ 1.0�{ ����vs�h������� 0.5�{
# �f��Ŗh����������牺���C�����l�A����Ŗh��Ȃ������������C���Ƃ��͂��Ȃ��́H �f��s���ő��ΓI�ɕ��펝���L���Ƃ������邯��
if ($y{gua}) {
	if ($m{wea}) {
		if (&is_gua_valid($y{gua},$m{wea})) {
			$m_at = int(0.5 * $m_at);
			$is_y_tokkou2 = 1;
		}
	}
	else {
		$m_at = int(0.3 * $m_at);
		$is_y_tokkou2 = 1;
	}
}
#else {
#	$m_at = int($m_at * 1.2) if $m{wea};
#}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})) {
			$y_at = int(0.5 * $y_at);
			$is_m_tokkou2 = 1;
		}
	} else {
		$y_at = int(0.3 * $y_at);
		$is_m_tokkou2 = 1;
	}
}
#else {
#	$y_at = int($y_at * 1.2) if $y{wea};
#}

#================================================
# Ҳݓ���
#================================================
&run_battle2;
#&run_battle;

&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# ���s����
#================================================
sub run_battle2 {
	if ($cmd eq '') {
		$mes .= '�퓬����ނ�I�����Ă�������<br>';
	}
	elsif ($m{turn} >= 20) { # �Ȃ��Ȃ��������Ȃ��ꍇ
		$mes .= '�퓬���E��݂𒴂��Ă��܂����c����ȏ�͐킦�܂���<br>';
		&lose;
	}
	else {
		# �������ƈ���ă^�[�����𖳎����Č��ʂ𔭊����鏈������������Ă���
		# ��U�E��U�ǂ����D�悵�ď������邩�ȑO�ɗ����̃t���O�Ǘ����s��

		# �܂������Ƒ���̍U���E�K�E�Z���� $m_s ������`�Ȃ玩���A$y_s ������`�Ȃ瑊��͍U��
		local $m_s = undef; # ��ڲ԰�̋Z�f�[�^������ ����`�Ȃ�U��
		local $pikorin; # ��ڲ԰���Z��M������ 1 �M���� 0 �M���ĂȂ�
		if (!$metal) { # ��ّ���ɂ͏�ɍU���ŕK�E�Z���M���Ȃ�
			$m_s = $skills[ $m_skills[ $cmd - 1 ] ] if $cmd > 0 && $guas[$m{gua}][0] ne '21'; # 1����ވȏ����͂��Ă��ċ���m�̊Z����Ȃ���ّ��肶��Ȃ��Ȃ�K�E�Z
			$m_s = undef if defined($m_s) && ($weas[$m{wea}][2] ne $m_s->[2] || !&m_mp_check($m_s)); # �K�E�Z��I�����Ă��Ă��������������MP������Ȃ��Ȃ�U��
			# �Z�M���Ă��t���O�������Ȃ����΍� �t���O���̂͐�U��U�֌W�Ȃ��̂ŗ\�ߑM���������ς܂��΃t���O���Ă���
			$pikorin = &_learning if !defined($m_s); # �U���ŋZ��M�����Ȃ�� 1 ���Ԃ�A�M�����Z�� $m_s �ɓ���
		}
		local $y_s = undef; # �G�̋Z�f�[�^������ ����`�Ȃ�U��
		$y_s = $skills[ $y_skills[ int(rand(6)) - 1 ] ] if $guas[$y{gua}][0] ne '21'; # ����m�̊Z����Ȃ��Ȃ�K�E�Z
		$y_s = undef if defined($y_s) && ($weas[$y{wea}][2] ne $y_s->[2] || !&y_mp_check($y_s) || $metal); # �K�E�Z��I�����Ă��Ă��������������MP������Ȃ��Ƃ���قȂ�U��

		# �t���O���܂��S���􂢏o���Ă��珈������Εςȋ������Ȃ��Ȃ�
		# ��
		#   �����Z��Ⱥ�ЂŔ��������MP������ɖ����Z�𔭊��ł���
		#   ��݋Z����ɶ��ЂŕԂ���Ă�����ɽ�݌��ʂ�^����
		# �퓬�� $who �Ŏ����Ƒ����؂�ւ��Ă�̂ł��ꓯ�l $who �Ńt���O�Ǘ����؂�ւ���

		local $who = '';
		$who = 'm';
		&get_battle_flags; # $m_is_guard, $m_is_stanch, ... �Ȃǂ����� skill.cgi �Q��
		$who = 'y';
		&get_battle_flags; # $y_is_guard, $y_is_stanch, ... �Ȃǂ����� skill.cgi �Q��

		# �����ōU���҂̽�݌��ʂ��I�t�ɂ���ν�݋Z���˃o�O�N���Ȃ��͂�
		# $m_is_stanch = 0 if $m_is_stanch && $y_gua_skill_mirror;
		# $y_is_stanch = 0 if $y_is_stanch && $m_gua_skill_mirror;

		# ��{�I�Ƀv���C���[�s���ɂȂ��Ă��邪�A��U��U�ŕ�����̂��ǂ��̂ł́H
		if ( rand($m_ag * 3) >= rand($y_ag * 3) ) { # �v���C���[��U
			$who = 'm';
			my $v = &attack;
			if ($y{hp} <= 0 && $m{hp} > 0) { # ؽ���Ұ�ނŎ�����HP0�ɂȂ��Ă��G�̍U���Ɉڂ遫
				&win; # ��ڲ԰��U������܂��͏������肾�Ǝv����
			}
			else {
				$who = 'y';
				&attack;
				if    ($m{hp} <= 0) { &lose; } # �����ؽ���Ұ�ނő��肪HP0�ɂȂ��Ă����łɎ�����HP0�Ȃ̂ŕ�����
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; } # ��ڲ԰��U�����珟�������ɂ�����H
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		else { # NPC��U
			$who = 'y';
			&attack;
			if ($m{hp} <= 0) { # ؽ���Ұ�ނœG��HP0�ɂȂ��Ă��������̍U���Ɉڂ遫
				&lose; # NPC��U������܂��͔s�k���肾�Ǝv����
			}
			else {
				$who = 'm';
				my $v = &attack;
				if    ($m{hp} <= 0) { &lose; } # �����ؽ���Ұ�ނł�������HP0�ɂȂ�ƕ�����
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; }
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		$m{turn}++;
	}
	$m{mp} = 0 if $m{mp} < 0;
	$y{mp} = 0 if $y{mp} < 0;
}

#=================================================
# �����̍U��
#=================================================
sub attack {
	my $temp_y = $who eq 'm' ? 'y' : 'm'; # �U�������u�����v�Ƃ����ꍇ�́u����v��ݒ�
	my $temp_y_name = ${$temp_y}{name};
	my $skill = ${$who.'_s'} if defined(${$who.'_s'});

	if ($who eq 'm' && $pikorin) { # �]��Ⱥ�Б���ɍU�����Ĕ�������ƋZ��M���Ȃ����� �M����������Ȃ��ɏC��
		${$who.'_mes'} = "�M����!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">���M��!!$m{name}��$m_s->[1]!!</font><br>|;
	}
	if ($who eq 'y' && $metal) {
		$mes .= "$y{name}�͗l�q�����Ă���";
		return;
	}
	if (${$temp_y.'_gua_avoid'}) { # �����Ⱥ�Д���
		$mes .= "$temp_y_name�͂Ђ��Ɛg�����킵��<br>";
		return;
	}

	my $hit_damage = ${$temp_y}{hp}; # �^�����_���[�W������
	if (defined($skill)) { # �K�E�Z
		if ($who eq 'm' && $pikorin) { # �]���ʂ�M�����Z��MP������Ȃ���Ζ����Z�Ȃǂ̃t���O����
			&{ $skill->[4] }($m_at);
		}
		else {
			# NPC���Ÿ���ׂ̂���肪�@�\���ĂȂ� �������邩��H
			${$who}{mp} -= $who eq 'm' && $guas[${$who}{gua}][0] eq '6' ? int($skill->[3] / 2) : $skill->[3];
			${$who.'_mes'} = $skill->[5] ? "$skill->[5]" : "$skill->[1]!" unless ${$who.'_mes'};
			$mes .= "${$who}{name}��$skill->[1]!!<br>";
			if (${$temp_y.'_is_guard'}) { # ���肪�����Z
				&{ $skill->[4] }(${$who.'_at'});
				${$temp_y}{hp} = $hit_damage;
			}
			elsif (${$temp_y.'_gua_skill_mirror'}) { # ���肪���˖h��
				&{ $skill->[4] }(${$who.'_at'});
				${$who}{hp} -= $hit_damage - ${$temp_y}{hp};
				$mes .= "������$guas[${$temp_y}{gua}][1]���Z�𔽎˂� ".($hit_damage - ${$temp_y}{hp})." ����Ұ�ނ������܂���!!<br>";
				${$temp_y}{hp} = $hit_damage;
			}
			else {
				&{ $skill->[4] }(${$who.'_at'});
			}
		}
	}
	else { # �U��
		my $sc = 1;
		if ($guas[${$who}{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		}
		elsif ($guas[${$who}{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "${$who}{name}�̍U��!!";
			my $kaishin_flag = ${$who}{hp} < ${$who}{max_hp} * 0.25 && int(rand(${$who}{hp})) == 0; # 999->249.75 && 0�`248 1/249
			$kaishin_flag = int(rand(${$who}{hp} / 10)) == 0 if $guas[${$who}{gua}][0] eq '8'; # 999->99.9 0�`98 1/99 �Ȃ�ƂȂ�1/3���炢�ŉ�S�ł�������łȂ���
			my $gua_mes;
			my $m_at_bf = ${$who.'_at'};
			if ($guas[${$who}{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[${$who}{gua}][1]���쓮����!";
				${$who.'_at'} = int(${$who.'_at'} * 1.2);
			}
			elsif ($guas[${$who}{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[${$who}{gua}][1]���\\������!";
				${$who.'_at'} = int(${$who.'_at'} * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin(${$who.'_at'}) : &_attack_normal(${$who.'_at'}, ${$temp_y.'_df'});
			${$who.'_at'} = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if (${$temp_y.'_is_counter'}) {
				$mes .= "�U����Ԃ��� $v ����Ұ�ނ������܂���<br>";
				${$who}{hp} -= $v;
			}
			elsif (${$temp_y.'_is_stanch'}) {
				$mes .= "��݂œ����Ȃ�!<br>";
			}
			else {
				$mes .= "$v ����Ұ�ނ��������܂���<br>";
				if ($who eq 'm' && $m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname�͉��Ă��܂���<br>" if $m{wea_c} == 0;
				}
				${$temp_y}{hp} -= $v;
			}
		}
	}
	$hit_damage -= ${$temp_y}{hp};

	# ���d���͎󂯂��_���[�W�ŉ񕜂���Ǝv���Ă����Ǘ^�����_���[�W�ŉ񕜂��� �����ď����Ă��邱�Ƃ���d�l�Ǝv����
	# ����ׂ͏���MP���������疳���Z�A�łł����b�󂯂��邪�A���d���͗^�����_���[�W�Ɉˑ�����̂Ÿ���ׂقǉ��b�󂯂Ȃ��Ǝv����
	# �����͂����݌����ĉ^���ǂ���θ���ׂ��������͗ǂ����c20����18,15�Ƃ��ɂ���̂́H
	if ($guas[${$who}{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "����������Ұ�ނ��� MP �� $v �z�����܂���<br>";
		${$who}{mp} += $v;
		${$who}{mp} = ${$who}{max_mp} if ${$who}{mp} > ${$who}{max_mp};
	}

	if (${$temp_y.'_gua_relief'} && $hit_damage) {
		my $v = int($hit_damage / 10);
		$mes .= "$v ����Ұ�ނ�h���܂���<br>";
		${$temp_y}{hp} += $v;
	}
	elsif (${$temp_y.'_gua_remain'} && $hit_damage && ${$temp_y}{hp} <= 0) {
		$mes .= "$guas[${$temp_y}{gua}][1]�ɍU�����������ՓI�ɒv�������܂̂��ꂽ<br>";
		${$temp_y}{hp} = 1;
	}
	elsif (${$temp_y.'_gua_half_damage'} && $hit_damage) {
		$mes .= "$guas[${$temp_y}{gua}][1]����Ұ�ނ𔼌������܂���<br>";
		${$temp_y}{hp} += int($hit_damage / 2);
	}
}

#=================================================
# �U���E�h���׸�
#=================================================
sub get_battle_flags { # $who �Ő؂�ւ� $who = 'm' or $who = 'y'
	return if ($guas[${$who}{gua}][0] eq '21') && ($who ne 'm' || !$pikorin); # ����m�̊Z�͍U������ �M���Ă�Ȃ狶��m�̊Z�ł��K�E�Z
	&{ ${$who.'_s'}->[6] } if defined(${$who.'_s'}); # �K�E�Z���׸�
	&{ $guas[ ${$who}{gua} ]->[6] } if ${$who}{gua}; # �h����׸�
}


#=================================================
# �����̍U��
#=================================================
sub m_attack2 {
	&y_flag2;

	if ($pikorin) { # �]��Ⱥ�Б���ɍU�����Ĕ�������ƋZ��M���Ȃ����� �M����������Ȃ��ɏC��
		$m_mes = "�M����!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">���M��!!$m{name}��$m_s->[1]!!</font><br>|;
	}
	if ($gua_avoid) { # �����Ⱥ�Д���
		$mes .= "$y{name}�͂Ђ��Ɛg�����킵��<br>";
		return;
	}

	local $who = 'm';
	my $hit_damage = $y{hp}; # �^�����_���[�W������

	if (defined($m_s)) { # �K�E�Z
		if ($pikorin) { # �]���ʂ�M�����Z��MP������Ȃ���Ζ����Z�Ȃǂ̃t���O����
			&{ $m_s->[4] }($m_at);
		}
		else {
			$m{mp} -= $guas[$m{gua}][0] eq '6' ? int($m_s->[3] / 2) : $m_s->[3];
			$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
			$mes .= "$m{name}��$m_s->[1]!!<br>";
			if($is_guard){
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$y{hp} = $pre_yhp;
			} elsif ($gua_skill_mirror) {
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$m{hp} -= $pre_yhp - $y{hp};
				$mes .= "������$guas[$y{gua}][1]���Z�𔽎˂� ".($pre_yhp - $y{hp})." ����Ұ�ނ������܂���!!<br>";
				$y{hp} = $pre_yhp;
			} else {
				&{ $m_s->[4] }($m_at);
			}
		}
	}
	else { # �U��
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}�̍U��!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0; # 999->249.75 && 0�`248 1/249
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0; # 999->99.9 0�`98 1/99 �Ȃ�ƂȂ�1/3���炢�ŉ�S�ł�������łȂ���
			}
			my $gua_mes;
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[$m{gua}][1]���쓮����!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$m{gua}][1]���\\������!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "�U����Ԃ��� $v ����Ұ�ނ������܂���<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "��݂œ����Ȃ�!<br>";
			}
			else {
				$mes .= "$v ����Ұ�ނ��������܂���<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname�͉��Ă��܂���<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$hit_damage -= $y{hp};

	# ���d���͎󂯂��_���[�W�ŉ񕜂���Ǝv���Ă����Ǘ^�����_���[�W�ŉ񕜂��� �����ď����Ă��邱�Ƃ���d�l�Ǝv����
	# ����ׂ͏���MP���������疳���Z�A�łł����b�󂯂��邪�A���d���͗^�����_���[�W�Ɉˑ�����̂Ÿ���ׂقǉ��b�󂯂Ȃ��Ǝv����
	# �����͂����݌����ĉ^���ǂ���θ���ׂ��������͗ǂ����c20����18,15�Ƃ��ɂ���̂́H
	if ($guas[$m{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "����������Ұ�ނ��� MP �� $v �z�����܂���<br>";
		$m{mp} += $v;
		$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v ����Ұ�ނ�h���܂���<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $y{hp} <= 0) {
		$mes .= "$guas[$y{gua}][1]�ɍU�����������ՓI�ɒv�������܂̂��ꂽ<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$y{gua}][1]����Ұ�ނ𔼌������܂���<br>";
		$y{hp} += int($hit_damage / 2);
	}

}

#=================================================
# ����̍U��
#=================================================
sub y_attack2 {
	&m_flag2;
	if ($metal) {
		$mes .= "$y{name}�͗l�q�����Ă���";
		return;
	}
	if ($gua_avoid) { # �����Ⱥ�Д���
		$mes .= "$m{name}�͂Ђ��Ɛg�����킵��<br>";
		return;
	}

	local $who = 'y';
	my $hit_damage = $m{hp}; # �^�����_���[�W������

	if (defined($y_s)) { # �K�E�Z
		$y{mp} -= $y_s->[3]; # NPC���Ÿ���ׂ̂���肪�@�\���ĂȂ� �������邩��H
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}��$y_s->[1]!!<br>";

		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
#			$mes .= "$guas[$m{gua}][1]���Z�𔽎˂���!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$mes .= "������$guas[$m{gua}][1]���Z�𔽎˂� ".($pre_mhp - $m{hp})." ����Ұ�ނ������܂���!!<br>";
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else { # �U��
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}�̍U��!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $gua_mes;
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes .= "<br>$guas[$y{gua}][1]���쓮����!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$y{gua}][1]���\\������!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "�U����Ԃ� $v ����Ұ�ނ��������܂���<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "��݂œ����Ȃ�!<br>";
			}
			else {
				$mes .= "$v ����Ұ�ނ������܂���<br>";
				$m{hp} -= $v;
			}
		}
	}
	$hit_damage -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "����������Ұ�ނ��� MP �� $v �z�����܂���<br>";
		$y{mp} += $v;
		$y{mp} = $y{max_mp} if $y{mp} > $y{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v ����Ұ�ނ�h���܂���<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $m{hp} <= 0) {
		$mes .= "$guas[$m{gua}][1]�ɍU�����������ՓI�ɒv�������܂̂��ꂽ<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$m{gua}][1]����Ұ�ނ𔼌������܂���<br>";
		$m{hp} += int($hit_damage / 2);
	}
}

#=================================================
# �U���E�h���׸�
#=================================================
sub get_battle_flags { # $who �Ő؂�ւ� $who = 'm' or $who = 'y'
	return if ($guas[${$who}{gua}][0] eq '21') && ($who ne 'm' || !$pikorin); # ����m�̊Z�͍U������ �M���Ă�Ȃ狶��m�̊Z�ł��K�E�Z
	&{ ${$who.'_s'}->[6] } if defined(${$who.'_s'}); # �K�E�Z���׸�
	&{ $guas[ ${$who}{gua} ]->[6] } if ${$who}{gua}; # �h����׸�
}

#=================================================
# �����̍U���׸�
#=================================================
sub m_flag2 {
	&init_battle_flags;
	return if ($guas[$m{gua}][0] eq '21') && !$pikorin; # ����m�̊Z�͍U������ �M���Ă�Ȃ狶��m�̊Z�ł��K�E�Z

	&{ $m_s->[6] } if defined($m_s); # �K�E�Z

	# �h��̓���t���O
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}

#=================================================
# ����̍U���׸�
#=================================================
sub y_flag2 {
	&init_battle_flags;
	return if $guas[$y{gua}][0] eq '21'; # ����m�̊Z�͍U������
	return if $metal;

	&{ $y_s->[6] } if defined($y_s); # �K�E�Z

	# �h��̓���t���O
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
}


#=================================================
# �U���׸ނ̏�����
#=================================================
sub init_battle_flags {
	$is_guard = 0; # HP�_���[�W"�K�E�Z"�̖����t���O
	$is_guard_s = 0; # �Ȃ�̃t���O���������
	$gua_relief = 0; # HP�_���[�W�̌y���t���O
	$gua_remain = 0; # HP0�̉���t���O
	$gua_half_damage = 0; # HP�_���[�W�̔����t���O
	$gua_skill_mirror = 0; # "�K�E�Z"�̔��˃t���O
	$gua_avoid = 0; # �s���̖����t���O
}

sub run_battle {
=pod
	if ($m{name} eq 'nanamie' || $m{name} eq '') {
		$m{mp} = 999;
		$m{ag} = 548;
		$y{mp} = 999;
		$m{act} = 0;
		$mes .= "m{wea} : $m{wea}, y{wea} : $y{wea}<br>";
		$mes .= "m{gua} : $m{gua}, y{gua} : $y{gua}<br>";
		$mes .= "skill_0 : $y_skills[0], skill_1 : $y_skills[1], skill_2 : $y_skills[2], skill_3 : $y_skills[3], skill_4 : $y_skills[4], skill_-1 : $y_skills[-1]<br><br>";
	}
=cut
	if ($cmd eq '') {
		$mes .= '�퓬����ނ�I�����Ă�������<br>';
	}
	elsif ($m{turn} >= 20) { # �Ȃ��Ȃ��������Ȃ��ꍇ
		$mes .= '�퓬���E��݂𒴂��Ă��܂����c����ȏ�͐킦�܂���<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $y_rand = int(rand(6))-1;
		# �Z��5�����ǁA5�Ԗڂ̋Z���I�΂��m��������(1/6, 1/6, 1/6, 1/6, 1/3)
		# �v���C���[�̍U���R�}���h���̃Y���C�����R�s�y�������ʊm���̕΂肪������s����Ǝv�������A
		# �Z��5���ׂĖ��߂ĂȂ��ꍇ�ɂ͍U���ɂȂ�m�����グ��悤�ɂ���Ӑ}������̂���
		# �Ȃ̂ŁA�Z���S�����܂��Ă�Ȃ��1/5���A�Z�����܂��ĂȂ��Ȃ�]���ʂ�U��������
		# ���񂮂炢�͗��Z�I�Ȃ��ƂƂ��ăX���[�ł��ǂ������H
#		my $y_rand = @y_skills >= 5 ? int(rand(5)) : int(rand(6))-1 ; # (-1, 0, 1, 2, 3, 4) -1�Ԗڂ̗v�f�̓P�c�Ȃ̂� 4 �Ɠ���
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&y_flag($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "y_flag<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		my $v = &m_attack;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "m_attack<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&m_flag;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_flag<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
			}
=cut
			&y_attack($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_attack<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
				$m{hp} = 1 if $m{hp} < 1;
			}
=cut
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		my $y_rand = int(rand(6))-1;
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&m_flag;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "m_flag<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
		}
=cut
		&y_attack($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$m{hp} = 1 if $m{hp} < 1;
			$mes .= "y_attack<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&y_flag($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_flag<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			my $v = &m_attack;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_attack<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# �����̍U��
#=================================================
sub m_attack {
	if ($gua_avoid) {
		$mes .= "$y{name}�͂Ђ��Ɛg�����킵��<br>";
		return;
	}
	
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	if ($guas[$m{gua}][0] eq '21') {
		$m_s = undef;
	}
	
	my $guard_pre_hp = $y{hp};
	
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩 # ���^�����肶��Ȃ���
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s) && !$metal) {
		if($guas[$m{gua}][0] eq '6'){
			$m{mp} -= int($m_s->[3] / 2);
		}else{
			$m{mp} -= $m_s->[3];
		}
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}��$m_s->[1]!!<br>";
		local $who = 'm';
		if($is_guard){
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$y{hp} = $pre_yhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$y{gua}][1]���Z�𔽎˂���!!<br>";
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$m{hp} -= $pre_yhp - $y{hp};
			$y{hp} = $pre_yhp;
		} else {
			&{ $m_s->[4] }($m_at);
		}
	}
	# �ߺ��! �K���Z5���� ���� �������� ���� ����̋������ʈȏな 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0 && !$metal) {
		local $who = 'm';
		&_pikorin;
	}
	else { # �U��
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}�̍U��!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0;
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0;
			}
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$m{gua}][1]���쓮����!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$mes .= "<br>$guas[$m{gua}][1]���\\������!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			
			if ($is_counter) {
				$mes .= "<br>�U����Ԃ��� $v ����Ұ�ނ������܂���<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>��݂œ����Ȃ�!<br>";
			}
			else {
				$mes .= "<br>$v ����Ұ�ނ��������܂���<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname�͉��Ă��܂���<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $y{hp};

	if ($guas[$m{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>�_���[�W��MP".int($guard_pre_hp / 20)."�Ƃ��ċz������<br>";
		$m{mp} += int($guard_pre_hp / 20);
		if ($m{mp} > $m{max_mp}) {
			$m{mp} = $m{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v ����Ұ�ނ�h���܂���<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $y{hp} <= 0) {
		$mes .= "<br>۹��������ĂɍU�����������ՓI�ɒv�������܂̂��ꂽ<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>�_���[�W�𔼌�������<br>";
		$y{hp} += int($guard_pre_hp / 2);
	}
	
}
#=================================================
# ����̍U��
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	
	if ($guas[$y{gua}][0] eq '21') {
		$y_s = undef;
	}
	if ($metal) {
		$mes .= "$y{name}�͗l�q�����Ă���";
		return;
	}
	
	if ($gua_avoid) {
		$mes .= "$m{name}�͂Ђ��Ɛg�����킵��<br>";
		return;
	}
	
	my $guard_pre_hp = $m{hp};
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}��$y_s->[1]!!<br>";

		local $who = 'y';
		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$m{gua}][1]���Z�𔽎˂���!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else {
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}�̍U��!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$y{gua}][1]���쓮����!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$mes .= "<br>$guas[$y{gua}][1]���\\������!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;

			if ($is_counter) {
				$mes .= "<br>�U����Ԃ� $v ����Ұ�ނ��������܂���<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>��݂œ����Ȃ�!<br>";
			}
			else {
				$mes .= "<br>$v ����Ұ�ނ������܂���<br>";
				$m{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>�_���[�W��MP�Ƃ��ċz������<br>";
		$y{mp} += int($guard_pre_hp / 20);
		if ($y{mp} > $y{max_mp}) {
			$y{mp} = $y{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v ����Ұ�ނ�h���܂���<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $m{hp} <= 0) {
		$mes .= "<br>$guas[$m{gua}][1]�ɍU�����������ՓI�ɒv�������܂̂��ꂽ<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>�_���[�W�𔼌�������<br>";
		$m{hp} += int($guard_pre_hp / 2);
	}
}

#=================================================
# �����̍U���׸�
#=================================================
sub m_flag {
	if ($guas[$m{gua}][0] eq '21') {
		return;
	}
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s)) {
		&{ $m_s->[6] };
	}
	# �h��̓���t���O
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}
#=================================================
# ����̍U���׸�
#=================================================
sub y_flag {
	if ($guas[$y{gua}][0] eq '21') {
		return;
	}
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	if ($metal) {
		return;
	}
	
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		&{ $y_s->[6] };
	}
	# �h��̓���t���O
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
}

#=================================================
# ��S�A�ʏ�U��
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>��S�̈ꌂ!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# �V�Z�K��(���łɊo���Ă���Z�ł�����) �K����1�A���K����0
#=================================================
sub _learning {
	if (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		# �o�����鑮���̂��̂�S��@lines�ɓ����
		my @lines = ();
		for my $i (1 .. $#skills) {
			push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
		}

		if (@lines) {
			my $no = $lines[int(rand(@lines))];
			# �o���Ă��Ȃ��Z�Ȃ�ǉ�
			my $is_learning = 1;
			for my $m_skill (@m_skills) {
				if ($m_skill eq $no) {
					$is_learning = 0;
					last;
				}
			}
			$m{skills} .= "$no," if $is_learning;
			$m_s = $skills[ $no ];
			return 1;
		}
		else { # ��O�����F�o��������̂��Ȃ�
			$m_mes = '�M�߂������őM���Ȃ��c';
		}
	}
	return 0;
}

sub _pikorin {
	# �o�����鑮���̂��̂�S��@lines�ɓ����
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "�M����!! $skills[$no][1]!";
		# �o���Ă��Ȃ��Z�Ȃ�ǉ�
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">���M��!!$m{name}��$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # ��O�����F�o��������̂��Ȃ�
		$m_mes = '�M�߂������őM���Ȃ��c';
	}
}


#=================================================
# �퓬�p���j���[
#=================================================
sub battle_menu {
	if($is_smart){
		$menu_cmd .= qq|<table boder=0 cols=5 width=90 height=90>|;

		$menu_cmd .= qq|<tr><td><form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="submit" value="�U��" class="button1s"><input type="hidden" name="cmd" value="0">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|</form>|;
		$menu_cmd .= qq|</td>|;

		for my $i (1 .. $#m_skills+1) {
			if($i % 5 == 0){
				$menu_cmd .= qq|<tr>|;
			}
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			my $mline;
			if(length($skills[ $m_skills[$i-1] ][1])>20){
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10,10). "\n" . substr($skills[ $m_skills[$i-1] ][1],20);
			}elsif(length($skills[ $m_skills[$i-1] ][1])>10) {
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10);
			}else{
				$mline = $skills[ $m_skills[$i-1] ][1];
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 5 == 4){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#m_skills % 5 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;
	}else{
		$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		$menu_cmd .= qq|<option value="0">�U��</option>|;
		for my $i (1 .. $#m_skills+1) {
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
		}
		$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|<input type="submit" value="�� ��" class="button1"></form>|;
	}
}


#=================================================
# ����
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}��|���܂���<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('battle');
	}

	$result = 'win';
}

#=================================================
# �s�k
#=================================================
sub lose {
	if ($m{name} eq 'nanamie' || $m{name} eq 'QE') {
#		&win;
#		return;
	}

	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}�͂���Ă��܂����c<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;

	$result = 'lose';
}


#=================================================
# ����ɂ����U�������ǂ���
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}

#=================================================
# �h��L�����ǂ���
#=================================================
sub is_gua_valid {
	my($gua, $wea) = @_;
	return $guas[$gua][2] eq $weas[$wea][2];
}

#=================================================
# MP�����邩�ǂ���
#=================================================
sub m_mp_check {
	my $m_s = shift;
	return ($m{mp} >= $m_s->[3] || ($guas[$m{gua}][0] eq '6' && $m{mp} >= int($m_s->[3] / 2)));
}
sub y_mp_check {
	my $y_s = shift;
	return ($y{mp} >= $y_s->[3] || ($guas[$y{gua}][0] eq '6' && $y{mp} >= int($y_s->[3] / 2)));
}



1; # �폜�s��
