#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# �����ē��_���ڍ�
# ���O�̕\�����~���Ə�������ւ��� ���O�t�@�C���ւ̏������ݏ���ς���̂���Ԃ����ʓ|�������̂ŕ\���ゾ������ւ��� 96�s�O�� ������������
#=================================================
&get_data;

$this_title  = "�����ē��[��";
$this_list   = "$logdir/chat_horyu_list";
$this_dir    = "$logdir/kaizou";
$this_script = 'chat_horyu_d.cgi';
$headline_script = 'chat_horyu.cgi';

# �A���������݋֎~����(�b)
$bad_time    = 5;

# �ő�۸ޕۑ�����
$max_log     = 50;

# �ő���Đ�(���p)
$max_comment = 2000;

# �Ñ�����
$remind_time = 7 * 24 * 3600;

# �Ñ�����
@no_remind = ($admin_name, $admin_sub_name);

# �N��ȊO�̒��ߐ؂茠����
@deletable_member = ($admin_name, $admin_sub_name);

#=================================================
&run;
&footer;
exit;

#=================================================
sub run {
	&write_comment if ($in{mode} eq "write") && $in{comment};
	&good_comment if ($in{mode} eq "good");
	&bad_comment if ($in{mode} eq "bad");
	&no_comment if ($in{mode} eq "no");
	&close_line if ($in{mode} eq "close");

	print qq|<form method="$method" action="$headline_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	my $rows = $is_mobile ? 2 : 5;
	open my $fh2, "< $this_dir/$in{line}.cgi" or &error("$this_dir/$in{line}.cgi ̧�ق��J���܂���");
	my $head_linet = <$fh2>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
	my @goods = split /,/, $bgood;
	my $goodn = @goods;
	my @bads = split /,/, $bbad;
	my $badn = @bads;
	if ($hidden) {
		$bgood = "����";
		$bbad = "����";
	}
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="line" value="$in{line}"><input type="hidden" name="target" value="$in{line}">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="��������" class="button_s"><input type="checkbox" name="tokumei" value="1">����<br>|;
	print qq|<input type="radio" name="mode" value="write" checked>��������|;
	if ($limit > $time + 7 * 24 * 3600) {
		print qq|<input type="radio" name="mode" value="close">�c�_����ߐ؂�<br>|;
		print qq|<select name="limit">|;
		print qq|<option value="1">�������</option>|;
		print qq|<option value="3">�����O��</option>|;
		print qq|<option value="7" selected>��������</option>|;
		print qq|</select><br>|;
	}
	print qq|<input type="radio" name="mode" value="good">�^��<input type="radio" name="mode" value="bad">����<input type="radio" name="mode" value="no">����<br>| if $limit > $time;
	print qq|<hr size="1">|;
	if($limit > $time + 7 * 24 * 3600){
		print qq|�c�_�i�K<br>������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad<br>\n|;
	}elsif($limit > $time){
		print qq|���̋c��ɏ�������<br>������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad<br>\n|;
	}else{
		if($goodn > $badn){
			print qq|<font size="5"><font color="blue">������]�� $goodn �l:$bgood</font> �������Ύ� $badn �l:$bbad ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}elsif($goodn < $badn){
			print qq|<font size="5">������]�� $goodn �l:$bgood <font color="red">�������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}else{
			print qq|<font size="5"><font color="yellow">������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}
	}
	my $last_write_time;
	my $second_line = '';
	my $contents = '';

	while (my $linet = <$fh2>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
		$bname .= "[$bshogo]" if ($bshogo && $bname ne '����������@���؎I');
		$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
		if ($hidden) {
			$bname = "����";
			$bicon = $default_icon;
			$bcountry = 0;
		}
		$bcomment = &comment_change($bcomment, 1);
#		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		if ($second_line) {
			$contents = qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n| . $contents;
		}
		else {
			$second_line = qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		}
		$last_write_time = $btime;
	}
	close $fh2;
	print $second_line;
	print $contents;
	print qq|</form>|;
#	if ($last_write_time + $remind_time < $time) {
#		&remind($in{line});
#	}
}

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, ">> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ̧�ق��J���܂���");

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"

	my $wname = $in{tokumei} ? '����������@���؎I' : $m{name};
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	print $fh "$time<>$date<>$wname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	close $fh;
	return 1;
}

#=================================================
# �Ǖ]��
#=================================================
sub good_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;

	if ($limit > $time) {
		my @goods = split /,/, $bgood;
		my @bads = split /,/, $bbad;
		$bgood = "";
		for my $gname (@goods){
			unless($gname eq $m{name}){
				if($bgood eq ""){
					$bgood .= "$gname";
				}else{
					$bgood .= ",$gname";
				}
			}
		}
		$bbad = "";
		for my $bname (@bads){
			unless($bname eq $m{name}){
				if($bbad eq ""){
					$bbad .= "$bname";
				}else{
					$bbad .= ",$bname";
				}
			}
		}
		if($bgood eq ""){
			$bgood .= "$m{name}";
		}else{
			$bgood .= ",$m{name}";
		}
	}

	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# ���]��
#=================================================
sub bad_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;

	if ($limit > $time) {
		my @goods = split /,/, $bgood;
		my @bads = split /,/, $bbad;
		$bgood = "";
		for my $gname (@goods){
			unless($gname eq $m{name}){
				if($bgood eq ""){
					$bgood .= "$gname";
				}else{
					$bgood .= ",$gname";
				}
			}
		}
		$bbad = "";
		for my $bname (@bads){
			unless($bname eq $m{name}){
				if($bbad eq ""){
					$bbad .= "$bname";
				}else{
					$bbad .= ",$bname";
				}
			}
		}
		if($bbad eq ""){
			$bbad .= "$m{name}";
		}else{
			$bbad .= ",$m{name}";
		}
	}

	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# ���]��
#=================================================
sub no_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;

	if ($limit > $time) {
		my @goods = split /,/, $bgood;
		my @bads = split /,/, $bbad;
		$bgood = "";
		for my $gname (@goods){
			unless($gname eq $m{name}){
				if($bgood eq ""){
					$bgood .= "$gname";
				}else{
					$bgood .= ",$gname";
				}
			}
		}
		$bbad = "";
		for my $bname (@bads){
			unless($bname eq $m{name}){
				if($bbad eq ""){
					$bbad .= "$bname";
				}else{
					$bbad .= ",$bname";
				}
			}
		}
	}
	
	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# �c�_����ߐ؂�
#=================================================
sub close_line {
	my $target = $in{target};
	my @voter = ();

	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;

	$limit = $time + $in{limit} * 24 * 3600;
	push @lines, "<><>$limit<>$hidden<>\n";
	$line = <$fh>;
	my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $line;
	my $aname = $bname;
	$aname =~ s/�����o<br>�c��//g;

	if ($aname ne $m{name} && $m{name} ne $cs{ceo}[$m{country}] && !&delete_check) {
		close $fh;
		return 1;
	}

	my ($lmin, $lhour, $lday, $lmon) = (localtime($limit))[1..4];
	$lmon += 1;
	$vcomment = "������" . $bcomment . "�̓��[������$lmon��$lday��$lhour��$lmin���ɐݒ肳��܂���<br>���[���܂��傤<hr>�y�����Ă��瑗�M�z";
	$bcomment .= "<br>�c�_����:$lmon��$lday��$lhour��$lmin��";

	push @lines, "$btime<>$bdate<>$bname<>$bcountry<>$bshogo<>$baddr<>$bcomment<>$bicon<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	$in{comment} = $vcomment;
	my $mname = $m{name};
	$m{name} = '�V�X�e��';
	my $mcountry = $m{country};
	$m{country} = 0;
	my $micon = $m{icon};
	$m{icon} = '';
	my $mshogo = $m{shogo};
	$m{shogo} = '';
	&send_group('all');

	$in{comment} = "";
	$m{name} = $mname;
	$m{country} = $mcountry;
	$m{icon} = $micon;
	$m{shogo} = $mshogo;

	return 1;
}

#=================================================
# �Ñ�
#=================================================
sub remind {
	$target = shift;
	open my $fh2, "< $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ̧�ق��J���܂���");
	my $head_linet = <$fh2>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
	my $head_linea = <$fh2>;
	my($atime,$adate,$aname,$acountry,$ashogo,$aaddr,$acomment,$aicon,$aid) = split /<>/, $head_linea;
	close $fh2;
	
	if ($limit < $time + 7 * 24 * 3600) {
		return;
	}
	
	$aname =~ s/�����o<br>�c��//g;
	
	for my $name (@no_remind) {
		if ($name eq $aname) {
			return;
		}
	}
	
	if (&system_letter($aname, "���Ȃ��̔��c�����c�_<br>$acomment<br>��7���Ԑi��ł܂���B")) {
		open my $fh3, ">> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ̧�ق��J���܂���");
		print $fh3 "$time<>$date<>�V�X�e��<>0<><><>���c�҂ɍÑ�����o���܂���<><>\n";
		close $fh3;
	}
}

sub system_letter {
	my $aname = shift;
	my $content = shift;

	my $send_id = unpack 'H*', $aname;
	local $this_file = "$userdir/$send_id/letter";
	if (-f "$this_file.cgi") {
		$in{comment} = $content;
		$mname = $m{name};
		$m{name} = '�V�X�e��';
		$mcountry = $m{country};
		$m{country} = 0;
		$micon = $m{icon};
		$m{icon} = '';
		$mshogo = $m{shogo};
		$m{shogo} = '';
		&send_letter($aname, 0);

		$in{comment} = "";
		$m{name} = $mname;
		$m{country} = $mcountry;
		$m{icon} = $micon;
		$m{shogo} = $mshogo;
		return 1;
	}
	
	return 0;
}

#=================================================
# ���؎҃`�F�b�N
#=================================================
sub delete_check {
	for my $name (@deletable_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}

