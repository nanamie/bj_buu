#!/usr/local/bin/perl --
require './config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# �莆 Created by Merino
#================================================

# �����炭���̒�`�����܂�Ӗ��Ȃ�
# letter.cgi �������ł̋����Ȃ�ΐ������������A�Ⴆ�Γ��L���Ă���莆�����ł���� blog.cgi �� $max_log �ɏ㏑������A������̃��O���ŎC��؂���
# send_letter �֐����� $max_log ������ɏ㏑������悤�ɂ����̂ŁA�������C�W��ꍇ�͂�������v�ύX
$max_log = 100; # �莆�̃��O��

&get_data;
&header_myroom;
if ($in{mode} eq 'delete_kiji' && $in{flag} == 1) { &delete_kiji; }
elsif ($in{mode} eq 'delete_kiji' && $in{flag} == 2) { &output_kiji; }
elsif ($in{mode} eq "write" && $in{comment}) { &_send_letter; }
elsif ($in{mode} eq "refuse") { &add_refuse; }
&letter_box;
&footer;
exit;

#================================================
sub _send_letter { # �莆�̑��M���� ��M���̕\���֐����ł���K�v����܂Ȃ�����������O�ɏo����
	my $rflag = 0;
	open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
		$rflag++ if $line eq $m{name};
	}
	close $fh;

	&send_letter($in{yname}, $in{is_save_log}) if $in{yname} ne $admin_name || $rflag == 0;
	print qq|<p>$in{yname} �Ɏ莆�𑗂�܂���$mes</p>|;

	# �v���C�o�V�[���l�����A�N���N�ɑ��M���������������M���O
	my $ltime = time();
	open my $fh, ">> $logdir/letter_log.cgi";
	print $fh "$m{name}<>$in{yname}<>$ltime\n";
	close $fh;
}

sub letter_box { # ���� get �� send �ŕʂ̊֐��ɕ����Ă������A��{�I�ɓǂݍ��ރ��O���Ⴄ���炢�łقړ����Ȃ̂ł܂Ƃ߂Ă��܂� ���Ă�̂Ɏ�M���Ƒ��M����2���`����̂��ʓ|
	my $month = (localtime($time))[4]; # �N���p
	&header_letter_box($month); # �u�莆�v����ͯ�ް

	if ($in{type} eq 'new_year' && $month eq '0' && -f "$userdir/$id/greeting_card.cgi") { # �N���
		&letter_box_greeting_card;
		return;
	}

	my $count = 0;
	my $this_file = $in{type} eq 'send' ? "$userdir/$id/letter_log.cgi" : "$userdir/$id/letter.cgi";
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��J���܂���");
	if ($in{type} eq 'send') { # ���M��
		&letter_box_send($fh, \$count);
	}
	else { # ��M��
		&letter_box_get($fh, \$count);
	}
	close $fh;

	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><select name="flag" class="menu1">|;
	print qq|<option value="1">�폜</option>|;
	print qq|<option value="2">�ۑ�</option>|;
	print qq|</select><input type="submit" value="���s" class="button_s"> ($count/$max_log)</p></form>|;

	my $letter_backup = "$userdir/$id/letter.txt";
		$letter_backup = "$userdir/$id/letter_log.txt" if $in{type} eq 'send';
	if (-f "$letter_backup") {
		my $backup_time = (stat $letter_backup)[9];
		my($min, $hour, $mday, $month) = ( localtime($backup_time) )[1..4];
		$month++;
		print qq|<a href="link.cgi?$letter_backup" target="_blank">�莆���ޯ�����̧��</a> �ޯ����ߓ� $month/$mday $hour:$min|;
	}

	if ($m{name} eq $admin_name && $in{type} ne 'new_year' && $in{type} ne 'send') { # ��M���ł͒���̫��
		print qq|<form method="$method" action="letter.cgi">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="no" value="$in{no}">|;
		print qq|�� <input type="text" name="rname" class="text_box1" value="$in{send_name}"><br>|;
		print qq|<input type="submit" value="refuse" class="button_s"></form>|;
		print qq|refuse list<br>|;
		open my $rfh, "< $logdir/refuse_list.cgi" or &error("$logdir/$id/letter.cgi̧�ق��J���܂���");
		while (my $line = <$rfh>) {
			print qq|$line<br>|;
		}
		close $rfh;
	}
}

sub letter_box_get {
	my ($fh, $count) = @_;
	my $rows = $is_mobile ? 2 : 8;
	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
	print qq|����於 <input type="text" name="yname" class="text_box1" value="$in{send_name}"><br>|;
	print qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="�莆�𑗂�" class="button_s">|;
	print qq|�@ <input type="checkbox" name="is_save_log" value="1" checked>���M���ɕۑ�</form><br>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		next if(($bcomment =~ /<hr>�y.*?�S���ɑ��M�z/ || $bcomment =~ /<hr>�y�����Ă��瑗�M�z/ || $bcomment =~ /<hr>�y���L.*?�ւ̺��āz/) && $in{type} eq 'ncountry'); # �l�� �S�ʂ������āA���L���Ȃ�next
		next if($bcomment !~ /<hr>�y.*?�S���ɑ��M�z/ && $in{type} eq 'country'); # �S�� �S�ʂ���Ȃ��Ȃ�next
		next if($bcomment !~ /<hr>�y���L.*?�ւ̺��āz/ && $in{type} eq 'diary'); # ���L ���L�ւ̺��Ă���Ȃ��Ȃ�next
		next if($bcomment !~ /<hr>�y�����Ă��瑗�M�z/ && $in{type} eq 'horyu'); # ������ �����Ă���Ȃ��Ȃ�next
		$bshogo = $bshogo ? "[$bshogo]" : '';
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;

		# �莆�̑��M�ҕ\�� �����̎莆�͑��M�҂̍������\��
		my $from_data = $bcountry eq '-1'
			? qq|From <a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>$bshogo <font size="1">($bdate)</font>|
			: qq|From <font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font><a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>$bshogo <font size="1">($bdate)</font>|
			;

		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|$from_data<hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
			# �f�U�C�������C�������Ȃ����Ǔ��������l����Ə̍���\���̓}�Y������
#			$bshogo = "" if $is_smart;
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|$from_data<br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$$count;
	}
}

sub letter_box_send {
	my ($fh, $count) = @_;
	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$$count;
	}
}

sub letter_box_greeting_card {
	my $pic_size = q|width="25px" height="25px"|;
	my $count = 0;
	open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("$userdir/$id/greeting_card.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my ($from_name, $from_id, $number) = split /<>/, $line;
		if ($is_mobile) {
			print qq|From $from_name<br>|;
			if ($number % 3 == 0) {
				print qq|��(��^o^)����������|;
			}
			elsif ($number % 3 == 1) {
				print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>���މ�V�N|;
			}
			else {
				print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
			}
			print qq|<br>���N�ʕt���N��󒊑I�ԍ� $number<br><hr><br>|;
		}
		else {
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			print qq|From $from_name</th></tr>|;
			print qq|<tr><td>|;
			if ($number % 3 == 0) {
				print qq|��(��^o^)����������|;
			}
			elsif ($number % 3 == 1) {
				print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>���މ�V�N|;
			}
			else {
				print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
			}
			print qq|<hr>���N�ʕt���N��󒊑I�ԍ� $number|;
			print qq|</td></tr></table><br>|;
		}
	}
	close $fh;
}

# �莆�̎�M���ݒ� ���ڐ��������� system.cgi �� set_letter_flag ���v�ύX
sub header_letter_box {
	my $month = shift;
	my $len = 5 - 1; # letter.cgi �̎�M���̐� - 1 �z��̏���l system.cgi �ł���` set_letter_flag
	my @letters = ();
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi" or &error('���̧�ق��J���܂���');
		my $line = <$fh>;
		close $fh;
		@letters = split /<>/, $line;
	}

	my $g_card_link;
	if ($month == 0) {
		$g_card_link = $in{type} eq 'new_year' ?  qq|/ �N���| : qq| / <a href="?id=$id&pass=$pass&no=$in{no}&type=new_year">�N���</a>|;
	}

	my $box_send_element = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=send">���M��</a>|;
	my @box_get_elements = ();
	$box_get_elements[0] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=get">���ׂ�|;
	$box_get_elements[1] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">�l��|;
	$box_get_elements[2] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=country">�ꊇ���M|;
	$box_get_elements[3] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=diary">���L��|;
	$box_get_elements[4] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=horyu">������|;
	$box_get_elements[$_] .= $letters[$_] ? "($letters[$_])</a>" : '</a>' for (0 .. $len);

	my $is_rewrite = 1;
	if ($in{type} eq 'ncountry') {
		$box_get_elements[1] = '�l��';
		$letters[1] = 0;
	}
	elsif ($in{type} eq 'country') {
		$box_get_elements[2] = '�ꊇ���M';
		$letters[2] = 0;
	}
	elsif ($in{type} eq 'diary') {
		$box_get_elements[3] = '���L��';
		$letters[3] = 0;
	}
	elsif ($in{type} eq 'horyu') {
		$box_get_elements[4] = '������';
		$letters[4] = 0;
	}
	elsif ($in{type} eq 'send') {
		$box_send_element = '���M��';
		$is_rewrite = 0;
	}
	else {
		$box_get_elements[0] = '���ׂ�';
		$letters[0] = 0;
	}

	my $is_delete = 1; # letter_flag.cgi ���폜���邩�ǂ���
	for my $i (0 .. $len) {
		$is_delete = 0 if $is_delete && $letters[$i]; # ���ǂ�����Ȃ�� letter_flag.cgi ���폜���Ȃ�
	}
	if ($is_rewrite && !$is_delete) { # letter_flag.cgi ���폜����Ȃ��Ȃ疢�Ǐ�Ԃ��X�V
		open my $fh, "> $userdir/$id/letter_flag.cgi" or &error('���̧�ق��J���܂���');
		my $line = '';
		$line .= "$letters[$_]<>" for (0 .. $len);
		print $fh $line;
		close $fh;
	}
	elsif ($is_delete) {
		unlink "$userdir/$id/letter_flag.cgi";
	}

	print qq|<p>|;
	print qq|��M��($box_get_elements[0] / $box_get_elements[1] / $box_get_elements[2] / $box_get_elements[3] / $box_get_elements[4]) / $box_send_element$g_card_link|;
	print qq|</p>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_all">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="�S�`�F�b�N" class="button_s"></p></form>|;
}

sub add_refuse {
	my @lines = ();
	open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgi̧�ق��ǂݍ��߂܂���");
	eval { flock $rfh, 2; };
	while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
		$rflag++ if $line eq $m{name};
		push @lines, "$line\n";
	}
	push @lines, "$in{rname}\n";
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;
}

#================================================
# �L���폜
#================================================
sub delete_kiji {
	return if @delfiles <= 0;
	
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$is_delete = 1;
				print "$bdate $bname�̎莆���폜���܂���<br>";
				splice(@delfiles, $i, 1);
				last;
			}
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

sub delete_all {
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 1;
		if($bcomment =~ /�S���ɑ��M�z/ && $in{type} eq 'ncountry') {
			$is_delete = 0;
		}
		if($bcomment !~ /�S���ɑ��M�z/ && $in{type} eq 'country') {
			$is_delete = 0;
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	print "�莆���폜���܂���<br>";
}

#================================================
# �L���ۑ�
#================================================
sub output_kiji {
	return if @delfiles <= 0;

	my $this_file = "$userdir/$id/letter.cgi";
		$this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';

	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon, @bcomments) = split /<>/, $line;
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$bshogo = $bshogo ? "[$bshogo] " : '';

				# �莆�̑��M�ҕ\�� �����̎莆�͑��M�҂̍������\��
				my $from_data = $bcountry eq '-1'
					? qq|From $bname $bshogo($bdate)|
					: qq|From $cs{name}[$bcountry] $bname $bshogo($bdate)|
					;

				$bcomment =~ s/<br>/\n/g;
				$bcomment =~ s/<hr>/\n\n/g;
				if (@lines) {
					push @lines, "\n\n$btime $from_data\n$bcomment";
				}
				else {
					push @lines, "$btime $from_data\n$bcomment";
				}
				splice(@delfiles, $i, 1);
				last;
			}
		}
	}
	close $fh;

	my $letter_backup = "$userdir/$id/letter.txt";
		$letter_backup = "$userdir/$id/letter_log.txt" if $in{type} eq 'send';

	open my $fh, "> $letter_backup" or &error("$letter_backup̧�ق��ǂݍ��߂܂���");
	print $fh @lines;
	close $fh;

	print qq|<a href="link.cgi?$letter_backup" target="_blank">�莆���ޯ�����̧��</a>|;
#	print "$userdir/$id/letter.txt";
}
