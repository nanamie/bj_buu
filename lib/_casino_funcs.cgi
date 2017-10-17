#================================================
# ���ɋ��p�֐�
#================================================

use constant GAME_RESET => 1; # �ްт̍X�V���~�܂��Ă���
use constant LEAVE_PLAYER => 2; # �Q���҂���è�ނɂȂ��Ă���

$_header_size = 5; # ͯ�ް�z����ް�����
($_state, $_lastupdate, $_participants, $_participants_datas, $_rate) = (0 .. $_header_size - 1); # ͯ�ް�z��̲��ޯ��

$limit_think_time = 60 * 10; # 10�����u����ڲ԰���O 60 * 10
$limit_game_time = 60 * 20; # 20�����u�Źް�ؾ�� 60 * 20

=pod
�ԍ��j�F����Ȋ����Ŏ��Ԃ��鎞�ɕ��C�Ȃ��`�����ނȂ肵�Ă���Ă݂Ă� (� : 9/10 21:53)
�ԍ��j�F�p�^�[���T�i�p�^�[���Q�Ő؂�J�[�h���W�ɂ��Ă݂�j (� : 9/10 21:52)
�ԍ��j�F�p�^�[���S�i�b�͔����{�^���ōX�V�A���̌�`�܂��͂a�̂��������̔Ԃ̃v���C���[���p�^�[���Q�j (� : 9/10 21:52)
�ԍ��j�F�p�^�[���R�i�b�͔����{�^���ōX�V�A���̌�`�܂��͂a���p�^�[���P�j (� : 9/10 21:51)
�ԍ��j�F�p�^�[���Q�i�b�͂��̂܂܍X�V�����ɑҋ@�A�`�܂��͂a�̂��������̔Ԃ̃v���C���[���J�[�h��؂�j�������΂������ (� : 9/10 21:51)
�ԍ��j�F��������p�^�[���P�i�b�͂��̂܂܍X�V�����ɑҋ@�A�`�܂��͂a�������ŃQ�[�����X�V�j (� : 9/10 21:50)
�ԍ��j�F�b�A30�b��Ɏ~�܂��Ă����n�����{������ (� : 9/10 21:49)
�ԍ��j�F�X�V����߂�O�ɂb�ɘA������30�b��ɑ�n���ɗ���悤���}�𑗂��Ă��� (� : 9/10 21:49)
�ԍ��j�FA�Ƃa�œK���ɃQ�[���i�߂āA��l�����ɍX�V����߂�i�����{�^���������Ȃ��j (� : 9/10 21:48)
�ԍ��j�FA��B�ŃQ�[���J�n�A�b�Ͷ��ɂ̊O�őҋ@ (� : 9/10 21:47)
�ԍ��j�F�v���C���[�R�l�p�ӂ���i�`�A�a�A�b�j (� : 9/10 21:47)
�ԍ��j�F�������炠��܂�h�m�o���Ȃ�����菇���������Ƃ��� (� : 9/10 21:47)
�ԍ��j�F��l�ŃQ�[���J�n����20�b�X�V���Ȃ��܂ܒN���ɉ{�����Ă�����Ăǂ��Ȃ邩���Ă݂��� (� : 9/10 21:43)
�ԍ��j�F�����A�ł�$is_reset�t���O�����Ă��Ă邩��A���̎��_�ł̓o�O��Ȃ� (� : 9/10 21:40)
�ԍ��j�Fif���̒���@non_active_players = &get_members($head[$_participants]); (� : 9/10 21:37)
�ԍ��j�F���[�A_casino_func.cgi��285�s�ڂ�if���̏�����$is_no_participants==true (� : 9/10 21:36)
�ԍ��j�F�ȂȂ݂��[�����ɋA���Ă���̂�����c�I (� : 9/10 21:13)
�ԍ��j�F�܂��ł�20�b�~�܂����Q�[�����Q���҂��{�������init_header���Ă΂�� (� : 9/10 21:11)
�ԍ��j�F���A�b�������� (� : 9/10 21:10)
�ԍ��j�F$limit_game_time��20�ɐݒ肳��Ă邯��$time�Ɓi�����j$head[$_lastupdate]���ă~���b���� (� : 9/10 21:03)
�ԍ��j�F$head[$_lastupdate] + $limit_game_time < $time (� : 9/10 21:03)
�ԍ��j�F_casino_func.cgi 285�s�ڂ��� (� : 9/10 21:01)
=cut

sub init_header {
	my $ref_arr = shift; # �̧�ݽ�� shift ����Ȃ��Ǝ擾�ł��Ȃ��i$_���Ǝ��̂�[0]�����o�����H�j
	$ref_arr->[$_] = '' for (0 .. $_header_size + $header_size - 1);
}

sub h_to_s { # ͯ�ް�z��𕶎���ɂ��ĕԂ�
	my @arr = @_;
	my $str = '';
	$str .= "$arr[$_]<>" for (0 .. $_header_size + $header_size - 1);
	return "$str\n";
}

sub d_to_s { # հ�ް�ް��𕶎���ɂ��ĕԂ�
	my @arr = @_;
	my $str = '';
	$str .= "$arr[$_]:" for (0 .. $#arr-1);
	return "$str$arr[$#arr];";
}

sub admin_reset {
	$m{c_turn} = 0;
	&write_user;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh '';
	close $fh;

	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	for my $game_member (@participants) {
		if ($game_member eq $m{name}) {
			$m{c_turn} = 0;
			&write_user;
		}
		else {
	 		&regist_you_data($game_member, 'c_turn', '0');
		}
	}
}

sub admin_reset2 {
	&regist_you_data($in{name}, 'c_turn', '0');
#	my $r = '';
#	my %p = &get_you_datas($in{name}, 0);
#	$mes .= "$in{name} c_turn $p{c_turn}";
#	my @members = ();

#	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
#	while (my $id = readdir $dh) {
#		next if $id =~ /\./;
#		next if $id =~ /backup/;

#		my %p = &get_you_datas($id, 1);
#		if ($p{c_turn} ne '0') {
#			my $name = pack 'H*', $id;
#			push @members, $name;
#			$r .= "$name $p{c_turn} ";
#		}
#	}
#	closedir $dh;

#	for my $i (0 .. $#members) {
#		&regist_you_data($members[$i], 'c_turn', '0');
#	}

	return $r;
}

=pod
��ȏ����̗���
_casino_funcs.cgi
	sub _default_run
		call &{$in{mode}} ۰�ް ����ނ̒l����֐����Ăяo��
		call @datas = &_get_menber
	sub _get_menber
		call &show_game_info(@datas)
	sub _participate �u�Q������v����
	sub observe �u�Q�����Ȃ��v����

this_file.cgi
	sub run
		call _default_run
	sub show_game_info(@datas)
	sub participate_form �u�Q������v��̫��
	sub participate �u�Q������v���� ڰĂ�n������
	sub start_game_form �u�J�n����v�u�Q�����Ȃ��v��̫��
	sub start_game �u�J�n����v���� ͯ�ް���`
	�u�Q�����Ȃ��v������_casino_funcs.cgi�Œ�`
	sub play_form ��ڲ��̫��
	sub play ��ڲ����
	�ȏ�̻��ٰ�݂������Ă���΂Ƃ肠��������
	sub &{$in{mode}} ���̑�۰�ް�ɑΉ����鏈��

show_game_info����ڲ��ʂȂǂ�\�� ������ͯ�ް�ް����n���Ă���
��ڲ��ʂŕ\���������ނ̒�`(���̺���ޒl���֐��Ƃ��ČĂяo��)
����ޒl����Ăяo�����֐����`
=cut

#================================================
# �ΐl���ɂ̊�{�I��Ҳ݉��
# $option_form �ɒǉ���̫�т�ݒ肵�Ă����Βǉ��ł���
#================================================
sub _default_run {
#	my $_default = $_; # ���ĕ����̗L��
	$in{comment} = &{$in{mode}} if $in{mode} && $in{mode} ne 'write'; # �e����ނɑΉ�����֐��ւ�۰�ް
	&write_comment if $in{comment};

	my ($member_c, $member, @datas) = &_get_member;

#	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;

	if ($m{c_turn}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="comment" value="������Ɨ���"><input type="hidden" name="mode" value="write">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="������Ɨ���" class="button_s">|;
		print qq|</form>|;
	}
	if ($m{name} eq 'nanamie') {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("admin_reset", "ؾ��");
		print qq|</form>|;

		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="text"  name="name" class="text_box_b"> հ�ް��|;
		print &create_submit('admin_reset2', 'c_turn');
		print qq|</form>|;
	}

	print $option_form;
#	}

	print qq|<h2>$this_title</h2>|;
	print qq|$mes|;
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;
	unless ($is_mobile) {
		print qq|�����۰��<select name="reload_time" class="select1"><option value="0">�Ȃ�|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]�b| : qq|<option value="$i">$reload_times[$i]�b|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c�l:$member</font><br>|;

	print qq|<font size="3">|;
	&_show_game_info(@datas);
	print qq|</font>|;

	print qq|<hr>|;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

#================================================
# �ΐl���ɂ����ް�Ǘ�
# show_game_info �ɓn���߂�l�̌Œ蕔�� ($m_turn, $m_value, $m_stock, $state, $lastupdate, $participants, $participants_datas, $rate)
# �ȍ~�̖߂�l�Ͷ��ɖ��̵ؼ����ް� �ؼ����ް����̂� start_game �Őݒ肷��
# $participants_datas �ɑS�Q���҂� name, value, stock ���������񂪓����Ă��� ex. name1:value1:stock1;name2:value2:stock2;
# $participants_datas �𑀍삷��K�v�͓��ɂȂ� ����ށ�_get_member�̏��ŌĂ΂��̂ŁA����ނ���ڲ԰�ް�������������΂��Ƃ͎����œǂݒ���
# $participants ����݂̗���������Ă���̂ŕ��я�����o�^�����t�Z�ł��Ȃ�
# ����ɁAmember.cgi �t�@�C���̕��я����Q�����ɂȂ��Ă���i��l�ڂ̎Q���ҁi�e�j�� member.cgi ��2�s��(1�s�ڂ�ͯ�ް)�A��l�ڂ̎Q���҂�3�s��...�j
#================================================
sub _get_member {
	my $member  = ''; # �Q���ҁE�{���҂Ȃǂ��ׂĂ���ڲ԰��������
	my @members = (); # ���̔z��
	my ($m_turn, $m_value, $m_stock) = (0, '', ''); # �����̃f�[�^
	my @active_players = (); # ��ڲ���̎Q���҂̔z��
	my @non_active_players = (); # ���O���ꂽ�Q���҂̔z��
	my $penalty_coin = 0; # ���O or ؾ�Ď�������è
	my $is_game = 0; # �ްт��J�n���Ă��邩

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	# ���ɂ��ް����
	# �ްт̏�ԁA�ްт̍ŏI�X�V���ԁA�ްт̎Q���ҁA�Q���҂��ް��AڰāA�ȍ~�Ͷ��ɖ��̵ؼ����ް�
	my @head = split /<>/, $head_line;
	my $is_no_participants = $head[$_participants] eq '';

	# �Q���҂��ް����͌Œ�Ȃ̂ŏ�ɐV�K�쐬
	# �Q���ҕ��������ݏ����\���̂ŏ���������K�v������
	$head[$_participants_datas] = '';

	my $is_member = 0 < $m{c_turn};
#	$mes .= "c_turn $m{c_turn}<br>";

	my %sames = ();
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if ($this_file =~ 'daihinmin' && $is_no_participants) { # �Q���҂����Ȃ�
			push @non_active_players, $mname if $mturn;
			if ($mname eq $m{name}) {
				$is_find = 1;
				push @members, "$time<>$m{name}<>$maddr<>0<><><>\n";
				$member .= "$mname($m{c_turn}),";
			}
			else {
				if ($time < $mtime + $limit_member_time) {
					push @members, "$mtime<>$mname<>$maddr<>0<><><>\n";
					$member .= "$mname($mturn),";
				}
			}
			next;
		}

		if ($mname eq $m{name}) {
			$is_find = 1;
			$member .= "$mname($m{c_turn}),";
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$mvalue<>$mstock<>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
			($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
			if ($is_member) {
				push @active_players, "$m{name}";
#				$head[$_participants] .= "$m{name}," if !$head[$_state];
				$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
			}
		}
		else {
#			$mes .= "name $mname<br>";
			my $is_entry = 0 < $mturn;
#			$mes .= "entry $mturn<br>";
			# ��è�ނȎQ���҂Ʊ�è�ނȉ{���҂����c��
			if ( ($is_entry && ($time < $mtime + $limit_think_time)) || ($time < $mtime + $limit_member_time) ) {
				$member .= "$mname($mturn),";
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
				if ($is_entry) {
					push @active_players, "$mname";
#					$head[$_participants] .= "$mname," if !$head[$_state];
					$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
				}
			}
			else {
				if ($is_entry && $is_member) { # �Q���҂�e����͎̂Q���҂̊m�F���K�v
					$head[$_participants] = &remove_member($head[$_participants], $mname); # �Q���ҕ����񂩂��è����ڲ԰�����O
					push @non_active_players, "$mname"; # ���O���ꂽ�Q���҂�ǉ�
					# �قڂقڃk�������p�H
#					$rate = $m{coin} unless $state; # ��ڲ���łȂ���Γq��������c������ڲ԰�̑S��݂�
				}
			}
		}
	}
	unless ($is_find) { # �������{���҂ɂ��Ȃ��Ȃ�ǉ�
		push @members, "$time<>$m{name}<>$addr<>0<><><>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
		($m_turn, $m_value, $m_stock) = (0, '', '');
		$member .= "$m{name}(0),";
		push @non_active_players, $m{name} if $m{c_turn};
	}

	my $is_reset = 0; # ��O�҂ɂ��ؾ�āFGAME_RESET�A�Q���҂ɂ��E���m�F�FLEAVE_PLAYER
	if (!$is_no_participants) { # �Q���҂�����
		if ($is_member) { # �Q���҂ɂ��۰�ނŹްт̍ŏI�X�V���Ԃ��X�V
			$head[$_lastupdate] = $time;
		}
		elsif ($head[$_lastupdate] && $m{c_turn} < 1 && ($head[$_lastupdate] + $limit_game_time < $time) && $head[$_participants]) { # ��Q���҂��~�܂��Ă���ްт��{��������ؾ��
			$is_reset = GAME_RESET;
			@non_active_players = &get_members($head[$_participants]);
			$penalty_coin = $head[$_rate] if $head[$_state]; # ���łɹްт��J�n���Ă����纲ݖv��
			$is_game = $head[$_state];
			&init_header(\@head);
			&reset_members(\@members);
		}
		if ($is_member && !$is_reset && 0 < @non_active_players) { # GAME_RESET�ŏ���������Ă��炸�A�Q���҂ƕ��u��ڲ԰������ꍇ
			$is_reset = LEAVE_PLAYER;
			$penalty_coin = $head[$_rate] if $head[$_state];
			$is_game = $head[$_state];
			if (@active_players == 1 && $is_game) {
				&init_header(\@head);
				&reset_members(\@members);
			}
		}
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_reset) { # ���u���ꂽ�ްт����u���Ă�����ڲ԰�̕Еt��
		for my $leave_player (@non_active_players) {
			# �ް�ؾ��
#			if ($is_reset eq GAME_RESET) {
#				&coin_move(-0.5 * $penalty_coin, $leave_player) if $penalty_coin;
#			}
#			elsif ($is_reset eq LEAVE_PLAYER) {
			if ($is_reset eq LEAVE_PLAYER) {
				if ($is_game) {
					my $cv = -1 * &coin_move(-1 * $penalty_coin, $leave_player);
					&coin_move($cv, $active_players[0]);
					&system_comment("��ڲ���̕��u��ڲ԰$leave_player�����O���܂���");
				}
				else {
					&system_comment("��W���̕��u��ڲ԰$leave_player�����O���܂���");
				}
			}
			&regist_you_data($non_active_players[$i], 'c_turn', 0);
		}
		if ($is_reset eq GAME_RESET) {
			&system_comment($is_game ? "���u���ꂽ��ڲ���̹ްт�ؾ�Ă��܂���" : '���u���ꂽ��W���̹ްт�ؾ�Ă��܂���');
		}
		elsif ($is_game && @active_players == 1) {
			if ($active_players[0] eq $m{name}) {
				$m{c_turn} = '0';
				&write_user;
			}
			else {
				&regist_you_data($non_active_players[$i], 'c_turn', 0);
			}
			&system_comment("�Q���҂�$active_players[0]�����ƂȂ������߹ްт�ؾ�Ă��܂���");
		}
	}
	elsif ($this_file =~ 'daihinmin' && $is_no_participants && @non_active_players) {
		for my $i (0 .. $#non_active_players) {
			if ($non_active_players[$i] eq $m{name}) {
				$m{c_turn} ='0';
				&write_user;
			}
			else {
				&regist_you_data($non_active_players[$i], 'c_turn', 0);
			}
		}
		&system_comment("���炩�̗��R�ɂ��ްт�ؾ�Ă���܂���");
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $m_turn, $m_value, $m_stock, @head);
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub _show_game_info {
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @participants = &get_members($head[$_participants]);

	if ($head[$_participants]) {
		&show_game_info($m_turn, $m_value, $m_stock, @head);
		print qq| �Q����:|;
		print qq|$participants[$_],| for (0 .. $#participants);
	}
	else {
		unless ($this_file =~ "chat_casino_s") {
			print qq|���ް��W��|; 
		}
	}
	&show_head_info($m_turn, $m_value, $m_stock, @head) if defined(&show_head_info); # ���ׂĂ���ڲ԰�ɕ\�����������1
	if ($head[$_state]) { # �ްт��J�n���Ă���
		&show_started_game($m_turn, $m_value, $m_stock, @head);
	}
	else { # �ްт��J�n���Ă��Ȃ�
		if (&is_member($head[$_participants], "$m{name}")) { # �ްтɎQ�����Ă���
			print qq|<br>|;
			&show_start_info($m_turn, $m_value, $m_stock, @head) if defined(&show_start_info); # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\�����������
			&_start_game_form($m_turn, $m_value, $m_stock, $head[$_participants]); # �J�n�E�Q�����Ȃ�̫��
		}
		else { # �ްтɎQ�����Ă��Ȃ�
			if ($max_entry <= @participants) { print qq|<br>�ްт̊J�n��҂��Ă��܂�|; } # �Q���҂����܂��Ă���
			else { # �Q���҂����܂��Ă��Ȃ�
				if (!$coin_lack && $m{coin} < $head[$_rate]) { print '<br>��݂�ڰĂɑ���Ă��܂���'; } # ��݂�����Ă��Ȃ�
				else { &participate_form(@participants) if defined(&participate_form); }
#				elsif ($head[$_participants]) { # �Q��̫��
#					&participate_form;
#				}
#				else { # �e̫��
#					&leader_form;
#				}
			}
		}
	}
	&show_tale_info($m_turn, $m_value, $m_stock, @head) if defined(&show_tale_info); # ���ׂĂ���ڲ԰�ɕ\�����������2
}

#================================================
# �ΐl���ɂ̐e�ɂȂ�
#================================================
sub _leader { # �u�e�ɂȂ�v����
	my ($in_rate, $m_value, $m_stock, $is_rate) = @_;

	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$is_find = 1;
			if (!$head[$_state] && @participants < $max_entry) {
				($mtime, $mturn, $mvalue, $mstock) = ($time, 1, $m_value, $m_stock);
				splice(@members, @participants, 0, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"); # ���ް̧�ُ�ŎQ������\�����邽�߂ɎQ���҂̌��Ɉړ�
			}
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
	}
	unless ($is_find) { # �������Ȃ��Ă����ȂǁA���ް̧�ُォ������Ă����ꍇ
		if (!$head[$_state] && @participants < $max_entry) {
			splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>1<>$m_value<>$m_stock<>\n");
		}
	}

	my ($is_entry, $is_entry_full, $is_no_coin) = (0, 0, 0);
	my $leader_mes = '';
	if ($max_entry <= @participants) {
		$is_entry_full = 1;
	}
	elsif (0 < $m{c_turn}) {
		$is_entry = 1;
	}
	elsif (!$is_rate && $m{coin} < $rate) {
		$is_no_coin = 1;
	}
	elsif (!$head[$_state] && $m{c_turn} == 0) { # ��W�l�����܂��Ă��炸���Q�����J�n�O�őΐl���ɂ�����Ă��Ȃ�
		unless ($participants[0]) { # �Q���҂����Ȃ��Ȃ�e
			$head[$_rate] = $in_rate;
			$head[$_participants] .= "$m{name},";
			$leader_mes = " ڰ�:$head[$_rate]";
			$head[$_lastupdate] = $time;
		}
		else {
			$head[$_participants] .= "$m{name},";
			$head[$_lastupdate] = $time;
		}
		$head[$_participants_datas] .= &d_to_s($m{name}, $m_value, $m_stock);
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($state) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif ($is_entry) {
		return "���łɎQ�����Ă��܂�";
	}
	elsif ($is_entry_full) {
		return "���łɎQ���҂��W�܂��Ă��܂�";
	}
	elsif ($is_no_coin) {
		return "��݂�ڰĂɑ���Ă��܂���";
	}
	elsif ($m{c_turn}) {
		return "�ΐl���ɂ���ڲ���ł�";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} ���Ȃɒ����܂���$leader_mes";
	}
}

#================================================
# �Q������̫��
#================================================
#sub participate_form {
#	print qq|<form method="$method" action="$this_script" name="form">|;
#	print &create_submit("participate", "�Q������");
#	print qq|</form>|;
#}

#================================================
# �ΐl���ɂɎQ������
#================================================
sub _participate { # �u�Q������v����
	my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;

	my @members = ();
	my $is_find = 0;
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);

	# ��݂�ڰĂɑ���Ă��ĕ�W�l�����܂��Ă��炸�J�n�O�̹ްтɎQ�����Ă��Ȃ�
	my $is_participate = @participants ? ($coin_lack || $head[$_rate] <= $m{coin}) : ($coin_lack || $in_rate <= $m{coin});
	$is_participate = $is_participate && !$head[$_state] && $m{c_turn} == 0 && @participants < $max_entry;

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$is_find = 1;
			if ($is_participate) { # �Q�������𖞂����Ă���
				splice(@members, @participants, 0, "$time<>$mname<>$maddr<>1<>$m_value<>$m_stock<>\n"); # ���ް̧�ُ�ŎQ������\�����邽�߂ɎQ���҂̌��Ɉړ�
			}
			else { push @members, "$time<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"; }
		}
		else { push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"; }
	}
	unless ($is_find) { # �������Ȃ��Ă����ȂǁA���ް̧�ُォ������Ă����ꍇ
		splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>1<>$m_value<>$m_stock<>\n") if $is_participate;
	}

	my $leader_mes = '';
	if ($is_participate) { # �Q�������𖞂����Ă���
		unless (@participants) { # �Q���҂����Ȃ��Ȃ�e
			# �ްі��̵ؼ���ͯ�ް��ݒ�
			$head[$_] = $tmp_head[$_-$_header_size] for ($_header_size .. ($_header_size+$header_size-1));

			$head[$_rate] = $in_rate;
			$head[$_participants] .= "$m{name},";
			$leader_mes = " ڰ�:$head[$_rate]";
			$head[$_lastupdate] = $time;
		}
		else {
			$head[$_participants] .= "$m{name},";
			$head[$_lastupdate] = $time;
		}
		$head[$_participants_datas] .= &d_to_s($m{name}, $m_value, $m_stock);
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($head[$_state]) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif ($m{c_turn}) {
		return "���łɎQ�����Ă��܂�";
	}
	elsif ($max_entry <= @participants) {
		return "���łɎQ���g�����܂��Ă��܂�";
	}
	elsif (!$coin_lack && $m{coin} < $head[$_rate]) {
		return "��݂�ڰĂɑ���Ă��܂���";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} ���Ȃɒ����܂���$leader_mes";
	}
}

#================================================
# �Q�����̑ΐl���ɂ��痣���
#================================================
sub _observe { # �u�Q�����Ȃ��v����
	$mes .= "_observe<br>";
	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my $is_observe = !$head[$_state] && $m{c_turn} == 1; # ��W���̹ްтɎQ�����Ă���
	my $me = '';

	if ($is_observe) {
		$head[$_participants] = '';
		$head[$_participants_datas] = '';
	}

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if (!$head[$_state] && $mturn == 1) { # ��W���̹ްтɎQ�����Ă���
			if ($m{name} eq $mname) {
				$me = "$time<>$mname<>$maddr<>0<><><>\n";
			}
			else {
				$head[$_participants] .= "$mname,";
				$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
				push @members, $line;
			}
		}
		else {
			push @members, $line;
		}
	}
	my @participants = &get_members($head[$_participants]);
	if ($me) {
		splice(@members, @participants, 0, $me); # ���ް̧�ُ�ŎQ������\�����Ă���̂ŁA�Ȃ𗣂ꂽ��Q���҂̌��Ɉړ�
	}
	elsif ($is_observe) {
		splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>0<><><>\n"); # ���ް̧�ُ�ŎQ������\�����Ă���̂ŁA�Ȃ𗣂ꂽ��Q���҂̌��Ɉړ�
	}

	my $is_reset = 0;
	unless ($head[$_participants]) { # ���ް�̍Ō�̈�l���Ȃ𗣂ꂽ��ؾ��
		$is_reset = GAME_RESET;
		&init_header(\@head);
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($head[$_state]) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif ($m{c_turn} == 0) {
		return "�ްтɎQ�����Ă��܂���";
	}
	else {
		$m{c_turn} = 0;
		&write_user;
		my $result_mes = "$m{name} ���Ȃ𗣂�܂���";
		if ($is_reset eq GAME_RESET) {
			&system_comment("$m{name} ���Ȃ𗣂ꂽ���߹ްт�ؾ�Ă��܂���");
			$result_mes = '';
		}
		return $result_mes;
	}
}

#================================================
# �J�n����E�Q�����Ȃ�̫��
#================================================
sub _start_game_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	my @participants = &get_members($participants);

	if ($participants[0] eq $m{name} && $min_entry <= @participants && @participants <= $max_entry) { # �Q���҂��K�v�\���Ȃ�J�n���ݕ\��
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("_start_game", "�J�n����");
		print qq|</form>|;
	}
	elsif ($participants[0] ne $m{name} && $min_entry <= @participants && @participants <= $max_entry) {
		print "�e�̹ްъJ�n��҂��Ă��܂�";
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("_observe", "�Q�����Ȃ�");
	print qq|</form>|;
}

#================================================
# �J�n�̋��ʏ���
#================================================
sub _start_game {
	my @members = ();
	my @game_members = ();

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @old_head = split /<>/, $head_line;

	# ̧������فAͯ�ް�A�S��ڲ԰�A�S�Q����
	&start_game($fh, \$head_line, \@members, \@game_members);

	unshift @members, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;


	if (!$old_head[$_state]) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 2;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '2');
			}
		}
	}
	return '�����I' if !$old_head[$_state];
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub reset_members {
	my $ref_members = shift;
	for my $i (0 .. $#$ref_members) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $ref_members->[$i];
		$ref_members->[$i] = "$mtime<>$mname<>$maddr<>0<><><>\n";
	}
}

#================================================
# �J�n�̋��ʏ���
#================================================
=pod
sub _start_game {
	my (@game_members) = @_;
	for my $game_member (@game_members) {
		if ($game_member eq $m{name}) {
			$m{c_turn} = 2;
			&write_user;
		}
		else {
	 		&regist_you_data($game_member, 'c_turn', '2');
		}
	}
	return '�����I';
}
=cut
#================================================
# ��݂̐؂�ւ�
#================================================
sub change_turn {
	my $participants = shift;
#	$mes .= "<br>member $participants";
	my $new_members = '';#"$participants[0],"; #$$participants = '';
	if ($participants) {
		my @participants = &get_members($participants);
		for my $i (1 .. $#participants) {
	#		$mes .= "i $i<br>";
			$new_members .= "$participants[$i],";# for (0 .. $#participants);
		}
		$new_members .= "$participants[0],";
	}
#	push @participants, splice(@participants, 0, 1);
#	my $new_members = ''; #$$participants = '';
#	$new_members .= "$participants[$_]," for (0 .. $#participants);
	return $new_members;
#	$$participants .= "$participants[$_]," for (0 .. $#participants);
#	$$participants =~ s/^(.*?),(.*)/$2$1,/; # ���쒆����ڲ԰���Ō���Ɉړ�
}

#================================================
# ��݂̑���
#================================================
sub coin_move{
# 811275
# 500611
	my ($add_coin, $name, $no_system_comment) = @_;
	return 0 if $add_coin == 0 || $add_coin eq '';
	return 0 unless &you_exists($name);

	# ������݂̎擾
	my $m_coin = $m{coin};
	if ($name ne $m{name}) { # ������݂̏��������Ώۂ����l�Ȃ�
		my %datas1 = &get_you_datas($name);
		$m_coin = $datas1{coin};
	}

	# �ړ��ł��麲ݐ��̎擾
	my $ret_v;
	if ($m_coin + $add_coin < 0) { # ������� + ������� �Ń}�C�i�X�ɂȂ�Ȃ�
		$ret_v = -1 * $m_coin; # ������݂͏�����݂����x
		$m_coin = 0; # ������݂� 0
	}
	elsif (2500000 < ($m_coin + $add_coin)) { # ������� + ���麲� �� 2500000 �𒴂���Ȃ�
		$ret_v = (2500000 - $m_coin); # ���麲݂� 2500000 �����x
		$m_coin = 2500000; # ������݂� 2500000
	}
	else { # ��݂̈ړ��ŏ����ł��麲݂̏���≺���Ɉ���������Ȃ�
		$ret_v = $add_coin;
		$m_coin += $add_coin;
	}

	# ������݂̐ݒ�
	if ($name eq $m{name}) {
		$m{coin} = $m_coin;
		&write_user;
	}
	else {
		&regist_you_data($name, 'coin', $m_coin);
	}
	&system_comment("$name �ړ������������ $add_coin �ړ���������� $ret_v ������� $m_coin");

=pod
	if ($name eq $m{name}) {
		if ($m{coin} + $add_coin < 0) { # ������� + ������� �Ń}�C�i�X�ɂȂ�Ȃ�
			$ret_v = -1 * $m{coin}; # ������݂͏�����݂����x
		}
		elsif (2500000 < ($m{coin} + $add_coin)) { # ������� + ���麲� �� 2500000 �𒴂���Ȃ�
			$ret_v = (2500000 - $m{coin}); # ���麲݂� 2500000 �����x
		}
		else { # ��݂̈ړ��ŏ����ł��麲݂̏�������Ɉ���������Ȃ�
			$ret_v = $add_coin;
		}
		$m{coin} += $ret_v;
		&system_comment("$m{name} �ړ������������ $add_coin ���ۂɈړ������麲� $ret_v");
		&write_user;
	}
	else {
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $add_coin; # ������� + �x������(�x����)���

		if ($temp < 0){ # ������� + ������� �Ń}�C�i�X�ɂȂ�Ȃ�
			$temp = 0; # ������ݖv��
			$ret_v = -1 * $datas1{coin}; # ������݂͏�����݂����x
		}
		elsif (2500000 < $temp) { # ������� + ���麲� �� 2500000 �𒴂���Ȃ�
			$ret_v = (2500000 - $datas1{coin}); # ���麲݂� 2500000 �����x
		}
		else { # ��݂̈ړ��ŏ����ł��麲݂̏�������Ɉ���������Ȃ�
			$ret_v = $add_coin;
			&system_comment("$name �ړ������������ $add_coin ���ۂɈړ������麲� $ret_v");
		}
		&regist_you_data($name,'coin',$temp);
		&system_comment("$name ������� $temp");
	}
=cut
#	$m_coin = -100
#	50 - 100
#	$ret_v = -50
#	

	unless ($no_system_comment) {
		if (-1 < $ret_v) { # �ړ���������݂��}�C�i�X�ł͂Ȃ�
			&system_comment("$name �� $ret_v ��ݓ��܂���");
		}
		else { # �ړ���������݂��}�C�i�X
			my $temp = -1 * $ret_v;
			&system_comment("$name �� $temp ��ݕ����܂���");
		}
	}

	# �x������(�x����)��݂����x����ꂽ(�x������)��݂�����
	# ���ۂɌ�҂��O�҂�葽���Ȃ�̂̓}�C�i�X�ł����l�����Ȃ��i100��������150���Ⴆ�邱�Ƃ͂Ȃ��j
	# 150��������100�������x�����Ȃ������悤�ȏꍇ�� -150�� < -100�� �ƂȂ��҂̂��傫���Ȃ�
	# �ł��ꉞ�}�C�i�X�Ȃ̂��m�F
=pod
	if ($add_coin < 0 && $ret_v < 0 && $add_coin < $ret_v) {
		$add_coin *= -1;
		my $diff = ($add_coin + $ret_v) * 10;
		&system_comment("�v�[�����玝���o����麲� $diff");

		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_file���J���܂���");
			eval { flock $fh, 2; };

			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff if 0 < ($pool - $diff);
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
=cut
	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# ���݂��Ȃ��ꍇ�̓X�L�b�v
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name �� $mes_as �Ƃ��� $prize ���l�����܂���");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name �� $mes_news</font>|);
	}
}

sub system_comment{
	my $s_mes = shift;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>�V�X�e�����b�Z�[�W<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������
#================================================
sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������(����հ�ް)
#================================================
sub you_lot_c_reset {
	my @names = @_;

	my @data = (
		['c_turn', 0],
		['c_value', 0],
		['c_stock', 0],
	);

	for $name (@names) {
		if ($name eq $m{name}) {
			$m{c_turn} = $m{c_value} = $m{c_stock} = 0;
			&write_user;
		}
		else {
			&regist_you_array($datas{name}, @data);
		}
	}
}

#================================================
# �T�u�~�b�g�{�^�� form�^�O�̊Ԃɋ���
#================================================
sub create_submit {
	my ($mode, $value) = @_;
	my $result_str = '';
	$result_str .= qq|<input type="hidden" name="mode" value="$mode">|;
	$result_str .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$result_str .= qq|<input type="hidden" name="guid" value="ON">|;
	$result_str .= qq|<input type="submit" value="$value" class="button_s">|;
	return $result_str;
}

#================================================
# �Z���N�g���j���[ form�^�O�̊Ԃɋ���
#================================================
sub create_select_menu {
	my ($name, $select, @menus) = @_;
	my $result_str = '';
	$result_str .= qq|<select name="$name" class="menu1">|;
	for my $i (0 .. $#menus) {
		my $select_str = ' selected' if $i == $select;
		$result_str .= qq|<option value="$i"$select_str>$menus[$i]</option>| if $menus[$i] <= $m{coin};
	}
	$result_str .= qq|</select>|;
	return $result_str;
}

#================================================
# ���W�I�{�^�� form�^�O�̊Ԃɋ���
#================================================
sub create_radio_button {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="radio" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

#================================================
# �`�F�b�N�{�b�N�X form�^�O�̊Ԃɋ���
#================================================
sub create_check_box {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="checkbox" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

sub get_members {
	my @members = split /,/, shift; # ���ް�ͺ�ϋ�؂�
	return @members;
}
sub remove_member {
	my ($game_members, $remove_name) = @_;
	my @game_members = &get_members($game_members);
	my $new_game_members = '';
	for my $i (0 .. $#game_members) {
		$new_game_members .= "$game_members[$i]," if $game_members[$i] ne $remove_name;
	}
	return $new_game_members;
}

sub is_member {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
#	my $is_find = 0;
	for my $i (0 .. $#game_members) {
		return 1 if $game_members[$i] eq $find_name;
#		if ($find_name eq $game_member) {
#			$is_find = 1;
#			last;
#		}
	}
	return 0;
}

sub is_my_turn {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
	return $find_name eq $game_members[0];

#	my ($target_str, $find_str) = @_;
#	$find_str = unpack 'H*', $find_str;
#	return $target_str =~ "^$find_str,";
}

sub get_member_datas {
	my @member_datas = split /;/, shift;
#	$members[$_] = pack 'H*', $members[$_] for (0 .. $#members);
	return @member_datas;
}

sub remove_member_datas {
	my ($game_member_datas, $remove_name) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		$new_game_member_datas .= "$game_member_datas[$i];" if $game_member_data[0] ne $remove_name;
	}
	return $new_game_member_datas;
}

sub update_member_datas {
	my ($game_member_datas, $name, $value, $stock) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		if ($game_member_data[0] eq $name) {
			$game_member_datas[$i] = "$name:$value:$stock";
		}
		$new_game_member_datas .= "$game_member_datas[$i];";
	}
	return $new_game_member_datas;
}

sub esc4re {
	my $str = shift;
	$str =~ s/([\x21\x24-\x26\x28-\x2b\x2e\x2f\x3f\x40\x5b-\x5e\x7b-\x7d])/\\$1/g if $str;
	return $str;
}

sub is_match {
	my ($target_str, $find_str) = @_;

	$target_str = &esc4re($target_str);
	$find_str = &esc4re($find_str);
	return $target_str =~ $find_str;
}

1;#�폜�s��
