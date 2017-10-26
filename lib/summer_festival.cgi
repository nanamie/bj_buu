$this_vote_file = "$logdir/pop_vote.cgi";
$this_vote2_file = "$logdir/pop_vote2.cgi";
$this_lot_file = "$logdir/event_lot.cgi";
$this_lot_name_file = "$logdir/event_lot_name.cgi";
$this_horror_story_file = "$logdir/horror_story.cgi";
$this_blog_vote_file = "$logdir/blog_vote.cgi";
$this_blog_vote_result_file = "$logdir/blog_vote_result.cgi";
$this_radio_dir = "$logdir/summer_radio";
#================================================
# �čՂ�
#=================================================
# ��X
@shop_list = (
#    cmd, ���i, ���z
	[1, '�H�ו�', 100000],
	[2, '��޹���', 100000],
	[3, '��', 50000],
);

# ��X�Ŕ��������
@shop_items = (
		#���,  �ԍ�, �ϋv�l�Ȃ�, ��, �m��
	[
		[2,1,0,0,50],		# ����Ѵ���
		[2,50,0,0,50],		# �������
		[3,23,0,0,10],		# ӺӺ
		[3,24,0,0,10],		# ���ް
		[3,65,0,0,10],		# ����
		[3,67,0,0,10],		# ��޽
		[3,76,0,0,5],		# ������
		[3,87,0,0,10],		# ����߷�
		[3,99,0,0,10],		# �ɳ
		[3,104,0,0,10],	# ���
		[3,169,0,0,10],	# ���
		[3,171,0,0,10],	# �ٸ
	],
);

# �󂭂��̒l�i
my $lot_money = 1000;

# ����܂̏ܕi
my $wea_no = 33; # л��

# �Ϻޏ܂̏ܕi
my $egg_no = 54; # ���ݴ���

# ���L��܏̍�
my $nikki_shogo = '���Ư�Ͻ��';

my @morning_glory_height = (
	# [0]����,	[1]���
	[10000, '���A�ǂ��܂ŐL�т�̂���H'],
	[300, '�Ԃ��炢���B������I'],
	[100, '�����L�тĂ���'],
	[50, '�t���o�Ă���'],
	[20, '�肪�o�Ă���'],
);

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if (&on_summer) {
		return 1;
	}
	else {
		$mes .= '�y�����͂��̉ċx�݂͏I������񂾂ˁc<br>';
		&refresh;
		&n_menu;
		return 0;
	}
}
#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɂǂ��s������?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�čՂ���͂���������<br>';
		$mes .= '�������悤��?<br>';
	}
	
	&menu('��߂�','�l�C���[�i��j', '��X', '�T�}�[�W�����{�󂭂�', '���a�I�̑�', '���L������', '�̎���', '�S����', '����琬', '�l�C���[�i���j');
}

sub tp_1 {
	return if &is_ng_cmd(1..9);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "���[��:$m{pop_vote}�[���L";
		$mes .= "���[�������镪�������[�ł����!<br>���[���͂����ȂƂ�������炦���!<br>";
		&menu('��߂�','���[');
	}
	elsif ($cmd eq '2') {
		$mes .= "����ȂƂ���ɖ�X�������!���������Ă��Ȃ�?<br>";
		&menu('��߂�', '����');
	}
	elsif ($cmd eq '3') {
		$mes .= '������荋�؂ȕ󂭂�����!<br>�K����l�͓��I����炵����!<br>';
		if (-f "$this_lot_name_file") {
			my @my_num = ();
			my $lot_amount = 0;
			open my $fh, "< $this_lot_name_file" or &error('�T�}�[�W�����{�t�@�C�����J���܂���');
			while (my $line = <$fh>) {
				my($name, $lot_num) = split /<>/, $line;

				if ($name eq $m{name}) {
					$lot_amount++;
					if (@my_num < 5) {
						push @my_num, $lot_num;
					}
				}
			}
			close $fh;
			if ($lot_amount) {
				$mes .= join ",", @my_num;
				if ($lot_amount >= 5) {
					$mes .= '��';
				}
				$mes .= '�v' . $lot_amount . '�������Ă����';
			}
		}
		&menu('��߂�', '����');
	}
	elsif ($cmd eq '4') {
		$mes .= '����6���ɂȂ�ƃ��W�I�̑�����Ă�炵����!<br>�X�^���v�W�߂悤!<br>';
		$mes .= "�X�^���v�F<br>";
		$mes .= qq|<table class="table2">|;
		$mes .= qq|<tr>|;
		for my $d (1..31) {
			$mes .= qq|<td>|;
			$mes .= qq|$d��:|;
			if (-f "$this_radio_dir/$d.cgi") {
				open my $fh, "< $this_radio_dir/$d.cgi" or &error('���W�I�̑��t�@�C�����J���܂���');
				while (my $line = <$fh>) {
					my($name, $rtime) = split /<>/, $line;

					if ($name eq $m{name}) {
						$mes .= qq|��|;
					}
				}
				close $fh;
			}
			$mes .= qq|</td>|;
			if ($d % 7 == 0) {
				$mes .= qq|</tr><tr>|;
			}
		}
		$mes .= qq|</tr>|;
		$mes .= qq|</table>|;
		&menu('��߂�', '�̑�����');
	}
	elsif ($cmd eq '5') {
		$mes .= '�����̎v���o����L�Ɏc����!<br>';
		if ($m{summer_blog}) {
			$mes .= "�����������F$m{summer_blog}����<br>";
		}
		&menu('��߂�', '����');
	}
	elsif ($cmd eq '6') {
		$mes .= '���؂�����N�O���A�̎����ɏo�����悤<br>';
		&menu('��߂�', '�s��');
	}
	elsif ($cmd eq '7') {
		$mes .= '���؂�����N�O���A�݂�Ȃŕ|���b�����悤<br>';
		&menu('��߂�', '���');
	}
	elsif ($cmd eq '8') {
		$mes .= '�������Ă悤!<br>';
		&menu('��߂�', '���');
	}
	elsif ($cmd eq '9') {
		$mes .= '��l��[�̐l�C���[!<br>';
		&menu('��߂�', '���[����');
	}
	else {
		&begin;
	}
}

#=================================================
# �l�C���[
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{pop_vote} > 0) {
		$mes .= '�N�ɓ��[���悤��?<br>';
		$mes .= qq|<form method="$method" action="$script"><p>���[����F<input type="text" name="vote_name" class="text_box1"></p>|;
		$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1" checked>���[����<br>|;
		$mes .= qq|<input type="text" name="num" value="1" class="text_box1"/>�[<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="���[" class="button1"></p></form>|;
		$m{tp} += 10;
	} else {
		$mes .= '���[�����Ȃ���c<br>';
		&begin;
	}
}

sub tp_110 {
	return if &is_ng_cmd(1);
	if ($in{vote_name} eq '') {
		$mes .= '���[�悪�L������ĂȂ���<br>';
		&begin;
		return;
	}
	if ($in{vote_name} eq $m{name}) {
		$mes .= '�����ɂ͓��[�ł��Ȃ���<br>';
		&begin;
		return;
	}
	
	my $vote_id = unpack 'H*', $in{vote_name};
	my $vote_num = $m{pop_vote} < $in{num} ? $m{pop_vote} : $in{num};

	if (-f "$userdir/$vote_id/user.cgi") {
		my @lines = ();
		my $is_find = 0;
		open my $fh, "+< $this_vote_file" or &error('�l�C���[�t�@�C�����J���܂���');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($name, $vote) = split /<>/, $line;

			if ($name eq $in{vote_name}) {
				$vote += $vote_num;
				$is_find = 1;
			}

			push @lines, "$name<>$vote<>\n";
		}
		unless ($is_find) {
			push @lines, "$in{vote_name}<>$vote_num<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$m{pop_vote} -= $vote_num;
		$mes .= "$in{vote_name} ����� $vote_num �[���ꂽ����������<br>";
		&refresh;
		&n_menu;
	} else {
		$mes .= '�N����?<br>';
		&begin;
		return;
	}
}



#=================================================
# ��X
#=================================================
sub tp_200 {
	return if &is_ng_cmd(1);
	$layout = 1;
	$mes .= '�����������H<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
 	$mes .= $is_mobile ? qq|<hr>���i/���z<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>���i</th><th>���z<br></th>|;

	for my $shop_ref (@shop_list) {
		my @shop = @$shop_ref;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$shop[0]">$shop[1]/$shop[2] G<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$shop[0]">$shop[1]</td><td align="right">$shop[2] G<br></td></tr>|;
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_210 {
	if ($cmd == 1) {
		$index = 1;
		for my $items_arr (@shop_items) {
			if ($index == $cmd) {
				my @items = @$items_arr;
				my $max_par = 0;
				for $item_ref (@items) {
					my @item = @$item_ref;
					$max_par += $item[4];
				}
				$r_par = int(rand($max_par)) + 1;
				my $par = 0;
				for $item_ref (@items) {
					my @item = @$item_ref;
					$par += $item[4];
					if ($par >= $r_par) {
						my $money = $shop_list[$cmd-1][2];
						if ($m{money} >= $money) {
							$m{money} -= $money;
							$mes .= $item[0] eq '1' ? "$weas[$item[1]][1]"
								  : $item[0] eq '2' ? "$eggs[$item[1]][1]"
								  : $item[0] eq '3' ? "$pets[$item[1]][1]"
								  : 				  "$guas[$item[1]][1]"
								  ;
							$mes .= '�𔃂�����!';
							&send_item($m{name}, $item[0],$item[1],$item[2],$item[3],1);
							my $v = int(rand(100) + 1);
							$m{pop_vote} += $v;
							$mes .= "���[����$v�����������";
						}
						last;
					}
				}
			}
			$index++;
		}
	}
	elsif ($cmd > 1) {
		if ($m{pet} == 0) {
			my $money = $shop_list[$cmd-1][2];
			if ($m{money} >= $money) {
				my $pet_index = $cmd*-1+1;
				$m{money} -= $money;
				$m{pet} = $pets[$pet_index][0];
				$m{pet_c} = $pets[$pet_index][5];
				$mes .= '�悭�������Ă邺�I�I<br>';
				my $v = int(rand($money*0.001) + 1);
				$m{pop_vote} += $v;
				$mes .= "���[����$v�����������";
			}
			else {
				$mes .= '�悭���Ă݂�I�@�[�j������˂����I�I<br>';
			}
		}
		else {
			$mes .= '�܂��͂��̘A��Ă����߯Ă�u���Ă��ȁI<br>';
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}
#=================================================
# �T�}�[�W�����{�󂭂�
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1);
	
	if ($m{money} >= $lot_money) {
		unless(-f "$this_lot_file"){
			open my $fh, "> $this_lot_file" or &error('�󂭂�̧�ق��ǂݍ��߂܂���');
			close $fh;
		}
		open my $fh, "+< $this_lot_file" or &error('�󂭂�̧�ق��ǂݍ��߂܂���');
		eval { flock $fh, 2 };
		$line = <$fh>;
		my($max_lot) = split /<>/, $line;
		$max_lot++;
		push @lines, "$max_lot<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		my $lot_num = sprintf("%06d", $max_lot);
		open my $fhn, ">> $this_lot_name_file" or &error('�󂭂�̧�ق��ǂݍ��߂܂���');
		print $fhn "$m{name}<>$lot_num<>\n";
		close $fhn;
		
		$m{money} -= $lot_money;
		if (rand(2) < 1) {
			$m{pop_vote}++;
			$mes .= "���[�������������";
		}
		$mes .= "������Ƃ�����!<br>";
	}
	else {
		$mes .= "����������Ȃ��c<br>";
	}
	&begin;
}

#=================================================
# ���W�I�̑�
#=================================================
sub tp_400 {
	return if &is_ng_cmd(1);

	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($hour eq '6') {
		if ($m{radio_time} + 23 * 3600 < $time) {
			mkdir "$this_radio_dir" or &error("$this_radio_dir ̫��ނ����܂���ł���") unless -d "$this_radio_dir";
			$mes .= '�^��������A�͂���������������!';
			open my $fh, ">> $this_radio_dir/$mday.cgi" or &error('���W�I�̑�̧�ق��ǂݍ��߂܂���');
			print $fh "$m{name}<>$time<>\n";
			close $fh;
			$m{radio_time} = $time;
			$m{act} = 0;
			my $v = int(rand(100) + 1);
			$m{pop_vote} += $v;
			$mes .= "���[����$v�����������";
		} else {
			$mes .= '�����͂����X�^���v�������';
		}
	} else {
		$mes .= '���W�I�̑��͒�6���̊Ԃ����ł��Ȃ��݂����c<br>';
	}
	&begin;
}

#=================================================
# �G���L
#=================================================
sub tp_500 {
	return if &is_ng_cmd(1);
	$layout = 2;
	if (&time_to_date($time) ne &time_to_date($m{blog_time})) {
		$mes .= qq|�����̎v���o����L�Ɏc����!<br>|;
		$mes .= qq|<form method="$method" action="blog.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="���L" class="button1"></form>|;
	} else {
		$mes .= '�����̓��L�͂�����������!<br>';
	}
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($wday eq '0') {
		$mes .= qq|���T�̓��L��܂����߂悤!<br>|;

		my $index = 0;
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $user_id = readdir $dh) {
			next if $user_id =~ /\./;
			
			if (-f "$userdir/$user_id/blog.cgi") {
				open my $fh, "< $userdir/$user_id/blog.cgi" or &error("���̂悤�ȓ��L�͑��݂��܂���");
				while (my $line = <$fh>) {
					$line =~ tr/\x0D\x0A//d;
					my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
					if ($btime > &date_to_time(&time_to_date($time - 7 * 24 * 3600)) && !$bicon) {
						$bcomment = join "<br>", @bcomment_arr;
						if ($is_mobile) {
							if ($index >= $m{stock} && $index < $m{stock} + 20) {
								$mes .= qq|<hr>�w$baddr�x$bname�̓��L<br>$bcomment|;
								$mes .= qq|<form method="$method" action="$script">|;
								$mes .= qq|<input type="hidden" name="cmd" value="$user_id:$btime:"><input type="submit" value="���̓��L�ɓ��[" class="button1">|;
								$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
								$mes .= qq|</form>|;
								$mes .= qq|<hr><br>|;
							}
						}
						else {
							$mes .= qq|<table class="table1" cellpadding="5" width="440">|;
							$mes .= qq|<tr><td>�w$baddr�x$bname�̓��L$bcomment</td>|;
							$mes .= qq|<td><form method="$method" action="$script">|;
							$mes .= qq|<input type="hidden" name="cmd" value="$user_id:$btime:"><input type="submit" value="���̓��L�ɓ��[" class="button1">|;
							$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
							$mes .= qq|</form></td></tr>|;
							$mes .= qq|</table><br>|;
						}
						$index++;
					}
				}
				close $fh;
			}
		}
		closedir $dh;
		if ($is_mobile) {
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="cmd" value="0"><input type="hidden" name="mode" value="prev"><input type="submit" value="�O��" class="button1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="cmd" value="0"><input type="hidden" name="mode" value="next"><input type="submit" value="����" class="button1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
		}
		
		$m{tp} += 10;
		&n_menu;
	} else {
		my $is_find = 0;
		unless(-f "$this_blog_vote_result_file"){
			open my $fh, "> $this_blog_vote_result_file" or &error('���L���[���ʃt�@�C�����J���܂���');
			close $fh;
		}
		open my $fh, "+< $this_blog_vote_result_file" or &error('���L���[���ʃt�@�C�����J���܂���');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($name, $date) = split /<>/, $line;
			if ($date eq &time_to_date($time - $wday * 24 * 3600)) {
				$is_find = 1;
			}

			push @lines, "$name<>$date<>\n";
		}
		unless(-f "$this_blog_vote_file"){
			open my $vfh, "> $this_blog_vote_file" or &error('���L���[�t�@�C�����J���܂���');
			close $vfh;
		}
		unless ($is_find) {
			%votes = ();
			open my $vfh, "< $this_blog_vote_file" or &error('���L���[�t�@�C�����J���܂���');
			while (my $line = <$vfh>) {
				my($name, $vote) = split /<>/, $line;
				my ($user_id, $btime) = split /:/, $vote;
				if ($btime > &date_to_time(&time_to_date($time - (7 + $wday) * 24 * 3600))) {
					$votes{$user_id}++;
				}
			}
			close $vfh;
			
			$max_vote = 0;
			$max_id = '';
			foreach my $key_id (keys(%votes)) {
				if ($max_vote < $votes{$key_id}) {
					$max_vote = $votes{$key_id};
					$max_id = $key_id;
				}
			}
			$max_name = pack 'H*', $max_id;
			&regist_you_data($max_name, 'shogo', $nikki_shogo);
			&write_send_news("���T�̓��L��܂�$max_name����ł�");
			
			$vote_date = &time_to_date($time - $wday * 24 * 3600);
			push @lines, "$max_id<>$vote_date<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		&begin;
	}
}

sub tp_510 {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($wday eq '0') {
		if ($cmd) {
			my ($cmd_id, $cmd_time) = split /:/, $cmd;
			unless (-f "$userdir/$cmd_id/blog.cgi") {
				&begin;
				return;
			}
			open my $bfh, "< $userdir/$cmd_id/blog.cgi";
			my $blog_find = 0;
			while (my $line = <$bfh>) {
				$line =~ tr/\x0D\x0A//d;
				my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
				if ($btime eq $cmd_time) {
					$blog_find = 1;
				}
			}
			close $bfh;
			unless ($blog_find) {
				$mes .= 'huga';
				&begin;
				return;
			}
			my @lines = ();
			my $is_find = 0;
			unless(-f "$this_blog_vote_file"){
				open my $fh, "> $this_blog_vote_file" or &error('���L���[�t�@�C�����J���܂���');
				close $fh;
			}
			open my $fh, "+< $this_blog_vote_file" or &error('���L���[�t�@�C�����J���܂���');
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $vote) = split /<>/, $line;
				if ($name eq $m{name}) {
					my ($user_id, $btime) = split /:/, $vote;
					if ($btime > &date_to_time(&time_to_date($time - 7 * 24 * 3600))) {
						$vote = $cmd;
						$is_find = 1;
					}
				}

				push @lines, "$name<>$vote<>\n";
			}
			unless ($is_find) {
				push @lines, "$m{name}<>$cmd<>\n";
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} else {
			if ($in{mode} eq 'prev') {
				$m{stock} -= 20;
				$m{stock} = 0 if $m{stock} < 0;
				$m{tp} -= 10;
				&tp_510;
				return;
			} elsif ($in{mode} eq 'next') {
				$m{stock} += 20;
				$m{tp} -= 10;
				&tp_510;
				return;
			}
		}
	}
	&begin;
}

#=================================================
# �̎���
#=================================================
sub tp_600 {
	return if &is_ng_cmd(1);
	$m{lib} = 'hunting_horror';
	$m{tp} = 0;
	&n_menu;
}

#=================================================
# �S����
#=================================================
sub tp_700 {
	return if &is_ng_cmd(1);
	$mes .= '�ق��̐l�̘b�𕷂�����A�����Řb������ł����<br>';
	$m{tp} += 10;
	&menu('��߂�','���', '����');
}

sub tp_710 {
	if ($cmd) {
		$layout = 2;
		if ($cmd eq '1') {
			$mes .= qq|<form method="$method" action="$script"><textarea name="comment"></textarea>|;
			$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
			$mes .= qq|<input type="radio" name="cmd" value="1" checked>���<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="���" class="button1"></form>|;
		}
		my $index = 0;
		open my $fh, "< $this_horror_story_file";
		while (my $line = <$fh>) {
			my($name, $story, $good, $bad) = split /<>/, $line;
			my @goods = split /,/, $good;
			my $goodn = @goods;
			my @bads = split /,/, $bad;
			my $badn = @bads;
			$index++;
			if ($m{stock} <= $index && $m{stock} + 10 > $index) {
				$mes .= $story;
				$mes .= qq|<br>|;
				$mes .= qq|��!:$goodn ��Ų!:$badn|;
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="cmd" value="2">|;
				$mes .= qq|<input type="hidden" name="index" value="$index">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="submit" value="��!" class="button1"></form>|;
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="cmd" value="3">|;
				$mes .= qq|<input type="hidden" name="index" value="$index">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="submit" value="��Ų!" class="button1"></form>|;
				$mes .= '<hr>';
			}
		}
		close $fh;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="cmd" value="4">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="�O��" class="button1"></form>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="cmd" value="5">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="����" class="button1"></form>|;
		$m{tp} += 10;
		&n_menu;
	} else {
		&begin;
	}
}

sub tp_720 {
	if ($cmd) {
		if ($cmd eq '1') {
			my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
			if ($hour < 1 || $hour > 3) {
				$mes .= "��鎞�Ԃ���Ȃ���<br>";
				&begin;
				return;
			}
			open my $fh, ">> $this_horror_story_file";
			print $fh "$m{name}<>$in{comment}<><><>\n";
			close $fh;
		} elsif ($cmd eq '2') {
			my $index = 0;
			my @lines = ();
			open my $fh, "+< $this_horror_story_file";
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $story, $good, $bad) = split /<>/, $line;
				$index++;
				if ($index == $in{index}) {
					my @goods = split /,/, $good;
					my $find = 0;
					for $g (@goods) {
						if ($g eq $m{name}) {
							$find = 1;
						}
					}
					if (!$find) {
						if ($good eq '') {
							$good .= "$m{name}";
						} else {
							$good .= ",$m{name}";
						}
					}
					push @lines, "$name<>$story<>$good<>$bad<>\n";
				} else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} elsif ($cmd eq '3') {
			my $index = 0;
			my @lines = ();
			open my $fh, "+< $this_horror_story_file";
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $story, $good, $bad) = split /<>/, $line;
				$index++;
				if ($index == $in{index}) {
					my @bads = split /,/, $bad;
					my $find = 0;
					for $b (@bads) {
						if ($b eq $m{name}) {
							$find = 1;
						}
					}
					if (!$find) {
						if ($bad eq '') {
							$bad .= "$m{name}";
						} else {
							$bad .= ",$m{name}";
						}
					}
					push @lines, "$name<>$story<>$good<>$bad<>\n";
				} else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} elsif ($cmd eq '4') {
			$m{stock} -= 10;
			$m{stock} = 0 if $m{stock} < 0;
			$m{tp} -= 10;
			&{'tp_' . $m{tp}};
			return;
		} elsif ($cmd eq '5') {
			$m{stock} += 10;
			$m{tp} -= 10;
			&{'tp_' . $m{tp}};
			return;
		}
	}
	$m{stock} = 0;
	&begin;
}

#=================================================
# ����琬
#=================================================
sub tp_800 {
	return if &is_ng_cmd(1);
	$m{tp} += 10;
	&menu('�A��', '�������', '�엿�����', '���̒��������');
}

sub tp_810 {
	unless ($m{morning_glory}) {
		$m{morning_glory} = 1;
	}
	$m{morning_glory}++ if rand(100) < 1;
	if ($m{morning_glory_time} + 24 * 60 * 60 < $time) {
		$m{morning_glory} += 5;
		$m{morning_glory_time} = $time;
	}
	$mes .= "���݂̍���:$m{morning_glory}mm<br>";
	for my $hi (0..$#morning_glory_height) {
		if ($m{morning_glory} >= $morning_glory_heigh[$hi][0]) {
			$mes .= $morning_glory_heigh[$hi][1] . '<br>';
			last;
		}
	}
	if ($cmd) {
		if ($cmd eq '3') {
			$m{tp} += 20;
			&{'tp_' . $m{tp}};
			return;
		}
		if ($cmd eq '1' && $eggs[$m{egg}][1] =~ /�����/) {
			$mes .= '���𒩊�ɂ�������';
			$m{egg} = 0;
			$m{morning_glory} *= 2;
		}
		if ($cmd eq '2' && $m{pet} > 0) {
			$mes .= $pets[$m{pet}][1] . '�𒩊�ɂ������';
			$m{tp} += 10;
			&menu('������', '�͂�');
			return;
		}
	}
	&begin;
}

sub tp_820 {
	if ($cmd && $m{pet} > 0) {
		$mes .= $pets[$m{pet}][1] . '�𒩊�ɂ�������';
		&remove_pet;
		$m{morning_glory} += 5;
	}
	&begin;
}

sub tp_830 {
	my @list = ();
	
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		
		my $name = pack 'H*', $pid;
		my %ys = &get_you_datas($pid, 1);
		if ($ys{morning_glory}) {
			push @list, "$name<>$ys{morning_glory}<>\n"
		}
	}
	closedir $dh;
	@list = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @list;
	my $i = 1;
	my $last_height = -1;
	for my $line (@list) {
		my ($name, $height) = split /<>/, $line;
		if ($i > 10 && $last_height != $height) {
			last;
		}
		$mes .= "$i�� $name����̒���F$height mm";
		for my $hi (@morning_glory_height) {
			if ($height >= $$hi[0]) {
				$mes .= $$hi[1] . '<br>';
				last;
			}
		}
		$mes .= '<hr>';
		$last_height = $height;
		$i++;
	}
	&begin;
}

#=================================================
# �l�C���[
#=================================================
sub tp_900 {
	return if &is_ng_cmd(1);
	
	$mes .= '�N�ɓ��[���悤��?<br>';
	$mes .= qq|<form method="$method" action="$script"><p>���[����F<input type="text" name="vote_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>���[����<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���[" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_910 {
	return if &is_ng_cmd(1);
	if ($in{vote_name} eq '') {
		$mes .= '���[�悪�L������ĂȂ���<br>';
		&begin;
		return;
	}
	if ($in{vote_name} eq $m{name}) {
		$mes .= '�����ɂ͓��[�ł��Ȃ���<br>';
		&begin;
		return;
	}
	
	my $vote_id = unpack 'H*', $in{vote_name};

	if (-f "$userdir/$vote_id/user.cgi") {
		my @lines = ();
		my $is_find = 0;
		unless (-f "$this_vote2_file") {
			open my $fh, "> $this_vote2_file" or &error('�l�C���[�t�@�C�����J���܂���');
			close $fh;
		}
		open my $fh, "+< $this_vote2_file" or &error('�l�C���[�t�@�C�����J���܂���');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($pop_name, $vote_name) = split /<>/, $line;

			if ($vote_name eq $m{name}) {
				$is_find = 1;
				$pop_name = $in{vote_name}
			}

			push @lines, "$pop_name<>$vote_name<>\n";
		}
		unless ($is_find) {
			push @lines, "$in{vote_name}<>$m{name}<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "$in{vote_name} ����ɓ��[����<br>";
		&refresh;
		&n_menu;
	} else {
		$mes .= '�N����?<br>';
		&begin;
		return;
	}
}

1; # �폜�s��
