use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_rampart.cgi'; # ���
#=================================================
# �푈���� Created by Merino
#=================================================
# war.cgi�ɂ����Ă��������ǂ����Ⴒ����ɂȂ肻���Ȃ̂ŕ���

# �~�o�l��
my $max_rescue = 1;

# m{value} �͕��m�̔{����D���͂̕␳�Ȃǎ��񂳂�Ă��Ă�₱������ɁA�i�R��ނ��y�ɋ��߂��Ȃ��̂ŕs��
# �i�R��ނ����₦��΂��������߂���̂ō��{�I�Ɏd�l�ύX������
# m{value} ��i�R��ނƍĒ�`���A0, 1, 2 �Ƃ��������� �������R�[�h�̕ύX�ӏ��������̂Œ��߂�i�����ް�ق̐i�R������̏����������l�b�N���j
# �ް�ق͐i�R���ɏ�����ĕ␳���|���Ă���̂Œ��e���̏�͖��֌W�A$m{value} �� * 3 ����Ă��邩���d�v �i�R��ނ��ǉ������ƃo�O�肻��
my $war_form = ($pets[$m{pet}][2] eq 'speed_down' && $m{unit} ne '18' && $m{value} >= 3) ? $m{value} / 3 : $m{value};
$war_form = ($war_form == 1.5) ? 2 : int($war_form); # �i�R��� �����F0 �ʏ�F1 �����F2

#=================================================
# ��������
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	
	my $is_rewrite = 0;

	# ��ɵ�ɂ�鑝�������c�����m�Ƃ��ĕԂ����Ȃ�
	$m{sol} -= ($rank_sols[11] - $rank_sols[$m{rank}]) * $m{value} if $m{sedai} <= 3 && $m{pet} eq '162' && $m{rank} < 11;

	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
#	if ($y{sol} > 0) {
#		$cs{soldier}[$y{country}] += int($y{sol} / 3);
#		$is_rewrite = 1;
#	}

	# ��ǃf�[�^�}
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# ����
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "�����S�łƂ����s���_�Ȕs�k�ׁ̈A$m{name}�ɑ΂���]����������������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";

	if($m{master_c} eq 'lose_c'){
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(21)+50) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "�������a���𗧔h�ɖ��߂��ׁA$m{name}�ɑ΂���]�����オ��܂���<br>";
		$mes .= "�����$v��$e2j{exp}����ɓ���܂���<br>";
	}
	
#	$cs{soldier}[$y{country}] += int($y{sol} / 3) if $y{sol} > 0;

	# ��ǃf�[�^�}
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	&down_friendship;

	# �A���œ��������ƍ��m��������
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( ( ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 ) || ( ($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2  || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		my $mname = &name_link($m{name});
		&write_world_news("$c_m��$mname��$c_y��$cs{prison_name}[$y{country}]�ɗH����܂���");
		&add_prisoner;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# �ދp
#=================================================
sub war_escape {
	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );
	&write_yran('war', 1, 1);

	# ��ɵ�ɂ�鑝�������c�����m�Ƃ��ĕԂ����Ȃ�
	$m{sol} -= ($rank_sols[11] - $rank_sols[$m{rank}]) * $m{value} if $m{sedai} <= 3 && $m{pet} eq '162' && $m{rank} < 11;
	$m{sol} = 0 if $m{sol} < 0;

	$cs{soldier}[$m{country}] += $m{sol};
#	$cs{soldier}[$y{country}] += int($y{sol} / 3);

	# ��ǃf�[�^�}
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# ����
#=================================================
sub war_win {
	my $is_single = shift;

	# �D�����ް�:�K���������ق���׽�B������A�v���̎��͊K�����Ⴂ�ق���׽
	my $v = ($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2')) ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	if ($m{pet} eq '193' && !($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) ) { # �����ł͂Ȃ��ް��ގ��A�K���␳�Ɛ���␳�ɐi�R�␳�̂�
		if (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # �v��:�㍑�L��
			if ($m{sedai} < 5) { # �v��������␳
				$v *= 3;
			}
			elsif ($m{sedai} < 10) { # �v��������␳
				$v *= 2.5;
			}
		}
		else {
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10; # ����␳
		}
		$v *= $m{value}; # �i�R�␳
	}
	else {
		# ��������Ȃ�����׽������ϲŽ�B�O���u�E�g���A�Í����̈Í����ɂ͐l���␳�Ȃ�
		unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country})) {
			$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 5;
		}

		# ����ɂ��D���͑���
		if (($w{world} eq '4' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '4' || $w{world_sub} eq '5')))) { # �\�N�A����
			$v *= 2.5;
		}
		elsif (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # �v��:�㍑�L��
			my $sum = 0;
			for my $i (1 .. $w{country}) {
				$sum += $cs{win_c}[$i];
			}
			$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
			if ($m{sedai} < 5) {
				$v *= 3;
			}
			elsif ($m{sedai} < 10) {
				$v *= 2.5;
			}
		}
		elsif (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) { # ����
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
			$v *= 1.2;
		}
		else {
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
		}

		# ��풆�Ȃ�2�{
		my $p_c_c = 'p_' . &union($m{country}, $y{country});
		$v *= 2 if $w{$p_c_c} eq '2';

		# ���ݒ�
		$v *= &get_modify('war');

		# ��Ǖ␳
		my ($r_v, $r_vv) = &get_rampart_modify($y{country}); # ��ǂɂ��D���́E�D������̕␳���Ԃ�
		$v *= $r_v;

		#��\�{�[�i�X
		# �Q�d�͒D����1.1�{
		$v = int($v * 1.1) if $cs{war}[$m{country}] eq $m{name};
		# �N��͒D����1.05�{�A�\�N���Ȃ��1.2�{
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			my $ceo_bonus = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
			$v = int($v * $ceo_bonus);
		}

		# �b��
		$v = &seed_bonus('red_moon', $v);

		# ����
		$v = $v * $m{value} * (rand(0.4)+0.8);

		# �푰�ްŽ
		$v = &seed_bonus('war_win', $v);
	}

	$v *= 1.5 if $m{unit} eq '18'; # �m�␳

	unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) { # �����ł͂Ȃ�
		# �m۷�A��������c��2���ȏ�̔{��۷�ł͂Ȃ�
		unless ( $m{pet} eq '12' && (($m{unit} eq '18') || (($m{unit} eq '7' || $m{unit} eq '8') && ($time + 2 * 24 * 3600 < $w{limit_time}))) ) {
			$v = &use_pet('war_result', $v);
		}
	}

	$v = 999 if $cs{extra}[$m{country}] eq '1' && $cs{extra_limit}[$m{country}] >= $time; # ���ފo��

	# �D���͏��
	if ($v !~ /^(\d)\1+$/) { # ��ۖ�(����۽�g�p���Ȃ�)
		if ($m{value} < 1) { # �������s
#			$v = $v > 200 ? int(rand(50)+150) : int($v);
			$v = $v > 200 ? int(rand(80)+120) : int($v);
		}
		else { # �ʏ�E����
			unless ($w{world} eq $#world_states - 5) { # �ّ��ł͂Ȃ�
				if ($m{unit} eq '18') {
					if ($time + 2 * 24 * 3600 > $w{limit_time}) { # ��������c��P��
						$v = $v > (2000 + $r_vv) ? int(rand(500+($r_vv*0.5))+1500+($r_vv*0.5)) : int($v);
					}
					else {
						$v = $v > (1500 + $r_vv) ? int(rand(500+($r_vv*0.5))+1000+($r_vv*0.5)) : int($v);
#						$v = $v > 1500  ? int(rand(200)+1300) : int($v);
					}
				}
				else {
					if ($time + 2 * 24 * 3600 > $w{limit_time}) { # ��������c��P��
						$v = $v > (1500 + $r_vv) ? int(rand(500+($r_vv*0.5))+1000+($r_vv*0.5)) : int($v);
#						$v = $v > 1500 ? int(rand(250)+1250) : int($v);
					}
					else {
#						$v = $v > 600  ? int(rand(200)+400) : int($v);
						$v = $v > (800 + $r_vv)  ? int(rand(200+($r_vv*0.5))+600+($r_vv*0.5)) : int($v);
					}
				}
			}
			else {
				$v = int($v);
			}
			# ����������߂Â��Ă�������׽
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}

	# �ŖS���̏ꍇ����
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty;
	}
	else {
		# ��ɵ�ɂ�鑝�������c�����m�Ƃ��ĕԂ����Ȃ�
		$m{sol} -= ($rank_sols[11] - $rank_sols[$m{rank}]) * $m{value} if $m{sedai} <= 3 && $m{pet} eq '162' && $m{rank} < 11;
		$m{sol} = 0 if $m{sol} < 0;

		$cs{soldier}[$m{country}] += $m{sol};
	}
	if ($cs{disaster}[$y{country}] eq 'paper' && $cs{disaster_limit}[$y{country}] >= $time) {
		$v += 100;
	}
	# ���̓f�[�^�}
	$cs{strong}[$m{country}] += ($w{world} eq '13' || $w{world} eq $#world_states - 2 || $w{world} eq $#world_states - 3) ? int($v * 0.75):$v;
	$cs{strong}[$y{country}] -= $v unless ($w{world} eq $#world_states - 5);
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	&write_yran(
		'strong', $v, 1,
		"strong_$y{country}", $v, 1,
		'win', 1, 1,
		'war', 1, 1
	);

	my $mname = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$mname = '������';
	}

	if ($w{world} eq $#world_states - 5) {
		$mes .= "$v��$e2j{strong}�𓾂܂���<br>";
		&write_world_news(qq|$c_m��$mname��<font color="#FF00FF"><b>$v</b> ��$e2j{strong}�𓾂鎖�ɐ���</font>�����悤�ł�|);
	} else {
		$mes .= "$c_y����$v��$e2j{strong}��D���܂���<br>";
		if ($is_single) {
			&write_world_news(qq|$c_m��$mname��$c_y�ɐN�U�A$y{name}�ƈ�R�����̖���������� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����ɐ���</font>�����悤�ł�|);
		}
		else {
			$m{value} < 1
				? &write_world_news(qq|���҂���$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
				: &write_world_news(qq|$c_m��$mname��$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
				;
		}
	}

	# ��ǃf�[�^�}
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	&after_success_action('war', $is_single);

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = int($vv * 0.55) if $w{world} eq $#world_states - 5; # �푈���ō��o���l int(40.99.. * 1.5) = 61 int(61 * 0.55) = 33
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}�ɑ΂���]�����傫���オ��܂���<br>";
	$mes .= "$vv��$e2j{exp}����ɓ���܂���<br>";

	if($m{master_c} eq 'win_c'){
		++$m{medal};
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(11)+20) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "���̌��т�傫�����`�����ׁA$m{name}�ɑ΂���]��������ɏオ��܂���<br>";
		$mes .= "�����$v��$e2j{exp}����ɓ���܂���<br>";
	}
	# ڽ���
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>1<>\n";
		close $fh;
	}

	&refresh;

	&daihyo_c_up('war_c'); # ��\�n���x

	# �Í�
	if ($w{world} eq $#world_states) {
		my @acs = ();
		for my $c (1 .. $w{country}-1) {
			push @acs, $c if $w{"p_".$c."_".$w{country}} != 1; # �Í��Ɠ�����g��łȂ���
		}
		# �αر���͈̂Í��̓��������Í���łڂ��Ɠ��������o�R���ĈÍ��ɓ���t���O�������Í������ɂȂ錻��
		my $ahoalia = 1;
		for my $ac (@acs) {
			$ahoalia = 0 if !$cs{is_die}[$ac]; # ���󑤂��ŖS���ĂȂ��Ȃ畕�󑤑S���ŖS�t���O���낷
		}
		if ($cs{strong}[$m{country}] >= $touitu_strong || # ���͂����ꍑ�͈ȏ�ɂȂ�����������
			($cs{strong}[$w{country}] <= 0 && $union ne $w{country}) || # ���������αر�΍�
			($ahoalia && $m{country} eq $w{country})) { # �������͕��󑤂����ׂĖŖS���Ă��邩
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
			# �Í����͖ŖS�Ɠ����ɓ��ꔻ��
			$ahoalia = 1;
			for my $ac (@acs) {
				$ahoalia = 0 if !$cs{is_die}[$ac]; # ���󑤂��ŖS���ĂȂ��Ȃ畕�󑤑S���ŖS�t���O���낷
			}
			if ($ahoalia && $m{country} eq $w{country}) { # ���󑤂����ׂĖŖS���Ă��邩
				# �Í��ɂ�镕�󃉃X�C�`�ŖS�ł�������t���O�������Ȃ�
				# �Í������O���ƕ��󃉃X�C�`�𕕈󑤂��ŖS������ƕ��󏟗��ɂȂ�i���ʂɍl������Í������j
				# ���ꏈ���̎d�l�ɂ��Ƃ���Ȃ̂Ŗ�����˂��܂������Ȃ�������u
				# ���󃉃X�C�`�𕕈󑤂��łڂ��A�Ȃ����Í����ɂ��̌�̒��e���Ȃ��Ȃ粽������Ȃ��ƈÍ��ɏ����ڂȂ��i���X�����Ȃ̂ł�������u�j
				&_touitu;
			}
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
=pod
		�������̈Í������
		elsif ( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			require './lib/vs_npc.cgi';
			&npc_war;
		}
		�Í��̍��͂� 30000 �ȏ�̎��� 1/4 �Ŷ��������
		�Í��̍��͂� 30000 �����Ȃ� 1/3 ���Ǝv���Ă����ǂ悭�l��������Z�Ȃ̂� (1/4) + (1/3) - (1/4*1/3) = 0.5 �Ŗ������̍ō���������� 50%
		���m���̉��@�藝 A��������m�� + B��������m�� - (A��B��������m��)
=cut
		else {
=pod
			�����̑����͖{���Í��̋���Ƃ͊֌W�Ȃ��Ǝv����
			�Í����A3���ɉ����悤��5���ɉ����悤��10���ɉ����悤�����󑤂̍����Ɋ֌W�Ȃ����푈���͓���
			�z�����Ă��鍑����������قǈÍ��s���ɂȂ肻�������A�D��������̒D���͂��グ��Εz������Ă��悤���Í��L���ɂ��邱�Ƃ͉\
			�������͂��������z������Ă�O��̒D���͂Ŕ�������̂ŕz�����Ă��鍑�������Ă��Í��̋���ɂ͊֌W�Ȃ������͂�
			���؎I�͕z���ŕ��󑤂̒D���͂�����I�ɏオ��悤�ɂȂ����̂ŁA�z�����Ă��鍑��������قǈÍ����s���ɂȂ遨�����ɂ���ĈÍ��̋��オ�ς���Ă��܂��A���ꂪ���؎I�̎d�l
			���_�A�����ɂ��Í��̋���̕ω��͕��󑤂̒D���͂ƈÍ��̒D���͂̍����o�Ă��܂����Ƃɂ��̂ŁA�Í��̋���̃o�����X��������Ȃ�J�E���^�[�������D���͂𒲐����������ǂ�
			�Ƃ͎v�����A���̒D���͂��ǂ��o�����X���Ηǂ��̂����F�ڕ�����Ȃ�
			�����������D���͏�����グ�Ă��邽�߁A�Í�������ɍ��킹�ĒP���ɏグ��Ηǂ����Ƃ����Ƃ����ł͂Ȃ�
			�Ⴆ�΁A1�����10����ł͒D���͂��Ⴂ�A����𖳎����Ė������̂悤�ȒD���͂Ŕ������Ă��܂��Ɨ��s�s�����������i�������͏�����Ⴂ���ߖڗ����Ȃ������j
			���Ƃ����āA�e�l�̒D���͂ɒ��ڂ�������x�[�X�ɔ�������ƕz����۷�Ȃǂ̑��݉��l�������
			���ʁA�J�E���^�[���łǂ��ɂ����邵���Ȃ��̂��c�Ƃ������ƂɂȂ�
			���؎I�ł͈Í��̎d���l���ŃJ�E���^�[���𒲐����Ă������A�e�I�ł̃Q�[�����𖳎����Ďd���l���� 6 �ō����������ŌŒ�ɂȂ��Ă��܂�����A�����̕ω��Ō��ς�����Ȃǂ����ƂȂ�
			���������Í��͈Í��̎d���l�������A�Í��̓������̐l���Ƃ������ғ����d�v�Ȃ͂��Ȃ̂ŁA���Ă����Ȃ��Ă��ǂ��悤�ȈÍ��̐l���ŋ��オ���܂�͈̂�a��
			�i�Í��̐l�����d�v�����ĂȂ����炱���d���l�� 0 �̊��SNPC���ɂ��ł���悤�Ȑ݌v�Ȗ󂾂��A�d���l�� 0 �ł��Í����Ă�j
			�����ƁA�Q�[�����ɍ��E����Ȃ��悤�Ȉ�肵���Í��̋���̃x�[�X�l���蓾����͖̂������ƍl���āA���ꍑ�͂ɒ��ڂ��Ă݂�
			���ꍑ�͂���������n�[�h���������قǃJ�E���^�[���������A���ꍑ�͂��Ⴍ����n�[�h�����Ⴂ�قǃJ�E���^�[�����Ⴍ
			�����ɂ���ē��ꍑ�͂��㉺����̂ŁA����������ɂ���ĈÍ��̋��オ�ς���Ă��܂��Ƃ����ʂ͂��邪�A
			���m���ŃJ�E���^�[���܂������Ƃ��Ă����ꍑ�͂��������Ă����Α�l�����Ȃ�͂��Ȃ̂ŁA�����炭�d���l�����̓Q�[�����ɉ����悤�Ɏ����Œ��߂���Ă����͂��H
			���́A�撣�葹�ɂȂ邱�Ƃ� �撣��Ί撣��قǃJ�E���^�[���������� �撣��Ȃ��قǃJ�E���^�[�����オ��
			�Ƃ͂����A�Í��J�n���_�ŏ��s���������܂��Ă���悤�ȏ�ԂŗV�Ԃ��͂���ۂǃ}�V�Ȃ͂� �Í��v���Ԃ�ɔR�������Ă������z����������
=cut
			my ($holy_strong, $dark_strong) = (0, 0);
			$holy_strong += $cs{strong}[$_] for (1 .. $w{country}-1); # �Í��ȊO�̑S����
			my $holy_strong_ave = int($holy_strong / ($w{country}-1)); # �Í����������ύ���
			$dark_strong += $cs{strong}[$w{country}]; # �Í��̍���

			# ��{�d�l �Í����͂����ꍑ�͂��牓���قǶ�������㏸
			my $divisor = $touitu_strong;
			# �Í��̍��͂�������قǶ�������ቺ
			# ���󑤂̕��ύ��͂������قǶ�������ቺ���邪�A�Í��������̍��͂Ƃ��ĕ��ύ��͂𑫂��Ă���i���z�����j
			# ���z�����Ƃ��č��͂𑫂��Ȃ��ꍇ�A�����炭�Í������鉣����ō��͂��ϓ������Ƃ��ɶ�������̕ϓ����������Ȃ�
			my $dividend = $touitu_strong-($dark_strong+$holy_strong_ave);
			# (���ꍑ�� - (�Í����� + ���󕽋ύ���)) / ���ꍑ��

			# ���̎d�l�ɕς������ڂ̎��A�����炭�ǂꂩ���@�\���ĂȂ�����
			# �I��钼�O�A���炩�ɕ���̕��ύ��͂����Í��̍��͂̕����Ⴉ�����̂ɏC��Ӱ�ނ��ۂ��Ȃ�����
			# if ���̗D��x���悭������Ȃ����{�CӰ�ނ̕��ɕ��򂵂Ă����H �Ƃɂ����C��Ӱ�ލŗD��� if ���ɏC��
			if ($dark_strong < $holy_strong_ave) { # ����̕��ύ��͂����Í��̍��͂��Ⴂ
				$divisor = 10; # �Í����ɂ��� �C��Ӱ��
				$dividend = 8; # �Í��̶������ 80% ���ڂ� 100 % ������
				# 8 / 10
			}
			else {
#				if ($touitu_strong < 50000 && ($touitu_strong*0.5) < $dark_strong) { # ���ꍑ�͂�5���؂��Ă��āA���Í��̍��͂����ꍑ�͂̔�����荂�� �v�͏I�Ղ��Í��̓���߂�
				# ��L���Ɠ��ꍑ�͂� 50000 ��؂�Ȃ��ƈÍ��̶��������̉����ꂸ�A�����������悤�ȎI�Ńv���C����Ɖ��X�Í���������������܂ܑ��蔲������
				if (($touitu_strong*0.7) < $dark_strong) { # �Í������ꍑ�͂�7����葽�����͂�ۗL���Ă��� �Í��̓���߂�
					$divisor += ($dark_strong+$holy_strong_ave); # �Í��Ƃ��̉��z�����̍��͂������قǶ�������ቺ
					# (���ꍑ�� - (�Í����� + ���󕽋ύ���)) / ((�Í����� + ���󕽋ύ���) / 2 + ���ꍑ��)
					# �����ŏI�ն�����������邪�A�߯ĘA�˂ŗ]�T�œ���_����͂�
					# �����œ���ł��Ȃ��Ă��C��Ӱ�ނ��邩��܂��Ȃ�Ƃ��Ȃ�͂� �͂�
				}
				elsif ($dark_strong < 30000) { # �Í��̍��͂�3���؂��Ă���Ȃ�{�CӰ��
					$divisor -= $holy_strong_ave / 2; # ����̕��ύ��͂������قǈÍ��̶�������㏸ �{�CӰ��
					# (���ꍑ�� - (�Í����� + ���󕽋ύ���)) / (���ꍑ�� - ���󍑗� / 2)
					$dividend = $divisor * 0.60 if 0.60 < ($dividend / $divisor); # �Í��̍ō�������� 60% ���ڂ͂������V�䂾���� �������ɓV��t���āA�C���� 80 �Ɉ�������
				}
			}
#			$divisor = 10; # �Í����ɂ��� �C��Ӱ��
#			$dividend = 10; # �Í��̶������ 80% ���ڂ� 100 % ������

#			my $div = $dividend / $divisor;
#			$mes .= "<br>������������Ȃ��̂Ŋm�F�p $dividend / $divisor = $div<br>";

			if (int(rand($divisor)) < int($dividend)) {
				require './lib/vs_npc.cgi';
				&npc_war;
			}
		}
	}
	# �I��
	elsif (($w{world} eq '13' || ($w{world} eq '19' && $w{world_sub} eq '13'))) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
	}
	# �s��ՓV
	elsif ($w{world} eq $#world_states - 2) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_touitu;
		}
	}
	# �O���u
	elsif ($w{world} eq $#world_states - 3) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
			$cs{strong}[$m{country}] += 3000;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
	}
	# �ّ�
	elsif ($w{world} eq $#world_states - 5) {
		my $strongest_country = 0;
		my $max_value = 0;
		for my $i (1 .. $w{country}) {
			if ($cs{strong}[$i] > $max_value) {
				$strongest_country = $i;
				$max_value = $cs{strong}[$i];
			}
		}
		if ($y{country} eq $strongest_country) {
			if (int(rand(3)) < 1) {
				my $steal_v = int(rand(15)+10) * 100; # �D������P�p����Ă�̂ő��߂�
				$steal_v = $cs{strong}[$strongest_country] if $steal_v > $cs{strong}[$strongest_country];
				$cs{strong}[$strongest_country] -= $steal_v;
				$cs{strong}[$m{country}] += $steal_v unless $strongest_country eq $m{country};
				&write_world_news("<b>سާ���݂̑嗒�I$cs{name}[$m{country}]��$cs{name}[$strongest_country]��$e2j{strong}�� $steal_v �D���܂���</b>");
			}
		}
		else {
			if (int(rand(3)) < 1) {
				my $type = int(rand(14));
				if ($type < 2) {
					for my $i (1..$w{country}) {
						next if $i eq $m{country};
						$cs{strong}[$i] -= int(rand(40)+40);
					}
					&write_world_news("<b>�e����$e2j{strong}��������܂���</b>");
				}
				elsif ($type < 3) {
					for my $i (1..$w{country}) {
						for my $j ($i+1..$w{country}) {
							$w{"f_${i}_${j}"} = int(rand(20));
							$w{"p_${i}_${j}"} = 2;
						}
					}
					&write_world_news("<b>���E�����J��ƂȂ�܂���</b>");
				}
				elsif ($type <= 11) {
					my @types = ('food', 100000, 'money', 100000, 'soldier', 50000);
					my $sub_type = int(rand(3)) * 2;
					$cs{$types[$sub_type]}[$m{country}] += $types[$sub_type+1];
					&write_world_news("$c_m��$e2j{$types[$sub_type]}��$types[$sub_type+1]�������܂���");
				}
			}
		}
	}
	# ����
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# �ŖS
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# ����
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '9' || ($w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13')))) ) {
		&_hukkou;
	}
	# �S��
	elsif (($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>سާ���݂̑嗒�I$cs{name}[$m{country}]��$cs{name}[$y{country}]��$e2j{$kkk}�� $vvv �D���܂���</b>");
	}

	if ($w{world} eq '19' && $w{sub_time} < $time) { # �����̏�ύX
		$w{world_sub} = int(rand(@world_states-4));
		$w{sub_time} = $time + 6 * 3600; # 6���Ԍ�
	}

	&write_cs;
	&n_menu;
}

#=================================================
# �S���ɒ��Ԃ�����Ȃ�~�o
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	my @y_names = ();
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country,$flag) = split /<>/, $line;
		if ($flag == 0 && $count < $max_rescue && ($country eq $m{country} || $union eq $country) && $country ne '0' ) {
			$is_rescue = 1;
			push @y_names, $name;
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	# ���ł܂�̧������ٕ��Ă��珔�X�̏���
	if ($is_rescue) {
		&write_yran('res', $count, 1);
		my $mname = $m{name};
		$mname = '������' if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16'));
		for my $i (1 .. $count) {
			my $name = $y_names[$i-1];
			$mes .= "$c_y�ɕ߂炦���Ă���$name���~�o���܂���<br>";
			&write_world_news("$c_m��$mname��$c_y�ɕ߂炦���Ă���$name�̋~�o�ɐ������܂���");
		
			# ڽ����׸ލ쐬
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgi̧�ق����܂���");
				close $fh2;
			}

			&c_up('res_c');
			&use_pet('rescue');

			if ($w{world} eq $#world_states-4) {
				require './lib/fate.cgi';
				&super_attack('rescue');
			}
		}
	}
}

#=================================================
# ����
#=================================================
sub _touitu {
	# �����[�C�����������d���ꏈ���h�~
	# ���N�������L�����ɂ�铝�ꂪ����Ă���Ƃ肠������I���ֈڍs
	# �����R�[�h�̓s�����Ȃ񂩁A���܂Ƀo�O��i�[���j
#	open my $fh, "< $logdir/legend/touitu.cgi" or &error("$logdir/legend/touitu.cgi ̧�ق��J���܂���");
#	my $line = <$fh>;
#	close $fh;
#	if ($line =~ /$world_name��$w{year}�N�y$world_states[$w{world}]�z.*$m{name}.*/) {
#		$m{lib} = 'world';
#		$m{tp}  = 100;
#		return;
#	}

	&c_up('hero_c');
#	&debug_log(\%w, 'touitsu_w');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];

	my $mname = &name_link($m{name});
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC�����̏���
			&mes_and_world_news("<em>�����B�̗���҂Ƃ���$world_name�嗤���x�z���邱�Ƃɐ������܂���</em>",1);
			&write_legend('touitu', "�[���ł��ڊo�߂�$cs{name}[$w{country}]�̖ҎҒB��$mname��M���Ƃ�$world_name�嗤���x�z����");
			&send_twitter("�[���ł��ڊo�߂�$cs{name}[$w{country}]�̖ҎҒB��$m{name}��M���Ƃ�$world_name�嗤���x�z����");
			$is_npc_win = 1;
		}
		else { # ���󍑑��̏���
			&mes_and_world_news("<em>���E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ���܂���</em>",1);
			&write_legend('touitu', "$c_m��$mname�Ƃ��̒��ԒB�����E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ����");
			&send_twitter("$c_m��$m{name}�Ƃ��̒��ԒB�����E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ����");

			require './lib/shopping_offertory_box.cgi';
			my %sames = ();
			for my $wc (@win_countries) {
				open my $cfh, "< $logdir/$wc/member.cgi" or &error("$logdir/$wc/member.cgi̧�ق��J���܂���");
				while (my $player = <$cfh>) {
					$player =~ tr/\x0D\x0A//d;
					next if ++$sames{$player} > 1;
					&send_item($player, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
				close $cfh;
			}
		}
	}
	elsif ($w{world} eq $#world_states-2) {
		&mes_and_world_news("<em>$world_name�嗤��񕪂���킢��$c_m��$mname�Ƃ��̒��ԒB�̏����ɏI�����</em>",1);
		&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
		&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		$w{win_countries} = $m{country};
	}
	elsif ($w{world} eq $#world_states-3) {
		&mes_and_world_news("<em>$world_name�嗤���O������킢��$c_m��$mname�Ƃ��̒��ԒB�̏����ɏI�����</em>",1);
		&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
		&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		$w{win_countries} = $m{country};
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name�嗤�𓝈ꂵ�܂���</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]������$mname��$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]������$mname��$world_name�嗤�𓝈ꂷ��");
			&send_twitter("$c_m$cs{name}[$union]������$m{name}��$world_name�嗤�𓝈ꂷ��");
		}
		else {
			&mes_and_world_news("<em>$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
			&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
}

#=================================================
# ����
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_m�𕜋������邱�Ƃɐ������܂���</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# �ŖS
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	$w{world_sub} = int(rand(@world_states-4));
	&mes_and_world_news("<b>$c_y��łڂ��܂���</b>", 1);

	# ����Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# ����ԕω�
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# �ŖS�����獑�͂�D�悵�����̔���
#=================================================
sub _penalty {
	# �ЊQ
	if ( (($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12')) && rand(3) < 1) || rand(12) < 1 ) {
		&disaster( $w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12') ); # ��N or ��(��N)�̂ݒǉ�����è
	}
}

#=================================================
# �F�D�xDown
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	$w{'f_'.$c_c} -= ($m{pet_c} - 10) if ($m{pet} eq '193' && $m{pet_c} > 10);
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10 && $y{country} ne $union) {
		$w{'p_'.$c_c} = 2;
		my $mname = &name_link($m{name});
		&write_world_news("<b>$c_m��$mname�̐i�R�ɂ��$c_y�ƌ���ԂɂȂ�܂���</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}

#=================================================
# �C���㏊���l��
#=================================================
sub modified_member {
	my $i = shift;
	return $cs{member}[$i] - $cs{new_commer}[$i];
}


1; # �폜�s��
