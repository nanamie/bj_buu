require 'lib/_write_tag.cgi';
#=================================================
# BBS,CHAT�⏕���ٰ�� Created by Merino
#=================================================

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;
	&error('�������݌���������܂���') if (!&writer_check);

	my $mcountry = $m{country};
	if ($this_file =~ /$userdir\/(.*?)\//) {
		my $wid = $1;
		if (-f "$userdir/$wid/blacklist.cgi") {
			open my $fh, "< $userdir/$wid/blacklist.cgi" or &error("$userdir/$wid/blacklist.cgi̧�ق��J���܂���");
			while (my $line = <$fh>) {
				my($blackname) = split /<>/, $line;
				if ($blackname eq $m{name}) {
					&error('������');
				}
			}
			close $fh;

		}
		# �������̎莆�͍�����\��
		# 0 ������݂ɂȂ�̂łƂ肠���� -1 �ɂ��� letter.cgi ���ŏ���
		# ��`���ł̎莆���X�͓����ɂ��Ȃ�
		$mcountry = '-1' if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) && $in{comment} !~ "<hr>�y��`���ւ̃��X�z");
	}

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	return 0 if $in{comment} eq $hcomment;
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("�A�����e�͋֎~���Ă��܂��B<br>���΂炭�҂��Ă��珑������ł�������");
	}
	push @lines, $head_line;

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}

	# ���̈ʒu�Ŕ��f����Ə���擾�ł���v���O��������̌Ăяo���ƁA
	# �����łȂ��v���O��������̌Ăяo���œ�����������������Ȃ�������
	# ����擾�ł���v���O��������̌Ăяo���������ꍇ�ɂ͋����I�ɓ����ɂȂ邽�߁A
	# �����葁���Ώ��@�Ƃ��āu<hr>�y��`���ւ̃��X�z�v���܂�ł���Ȃ�Γ����ɂ͂��Ȃ�
	if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) && $in{comment} !~ "<hr>�y��`���ւ̃��X�z") {
		$mname = "������";
	}

	my %bbs_config = ();
	$bbs_config{shogo_limit} = 16;
	my $this_config = $this_file . '_config.cgi';
	if (-f $this_config) {
		open my $fhc, "< $this_config" or &error("$this_config ̧�ق��J���܂���");
		my $config_line = <$fhc>;
		for my $config_hash (split /<>/, $config_line) {
			my($k, $v) = split /;/, $config_hash;
			$bbs_config{$k} = $v;
		}
	}
	my $mshogo = length($m{shogo}) > $bbs_config{shogo_limit} ? substr($m{shogo}, 0, $bbs_config{shogo_limit}) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$mcountry<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('voice');
	}
	
	return 1;
}


#=================================================
# ���ް�擾
#=================================================
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub writer_check {
	if (@writer_member > 0) {
		for my $member (@writer_member) {
			if ($m{name} eq $member) {
				return 1;
			}
		}
		return 0;
	}
	return 1;
}

1; # �폜�s��