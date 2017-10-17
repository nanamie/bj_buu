#!/usr/local/bin/perl --
use Time::HiRes;
$load_time = Time::HiRes::time unless $load_time;
use CGI::Carp qw(fatalsToBrowser);
require 'config.cgi';
require 'config_game.cgi';
#================================================
# Ҳ�CGI Created by Merino
#================================================
&get_data;
&error("��������ݽ���ł��B���΂炭���҂���������(�� $mente_min ����)") if ($mente_min);
&before_bj;
if ($m{wt} > 0) { # �S������
	# �S�����ɂł���s����̧�ق̒�`
	my @menus = (
		['���l�̂��X',	'shopping_akindo'],
		['�����݉��',	'shopping_auction'],
		['�ޯ�ϰ���',	'shopping_akindo_book'],
		['���̉攌��',	'shopping_akindo_picture'],
	);

	# �S�����̍s��
	if ($m{lib_r} ne '' && -f "./lib/$m{lib_r}.cgi") { # lib_r �Ăяo��
		if ($m{tp_r} eq '1' && $cmd eq '0') { # begin�ƭ���0(��߂�)��I������ݾ�
			$m{lib_r} = $m{tp_r} = '';
		}
		else {
			if ($m{tp_r}) { # lib_r ����
				require "./lib/$m{lib_r}.cgi";
				&{ 'tp_'.$m{tp_r} } if &is_satisfy; # is_satisfy��1(true)�Ȃ珈������
			}
			else { # begin �ƭ�
				&b_menu(@menus);
			}
		}
	}
	else {
		&b_menu(@menus) if defined($cmd);
	}

	# �e�X�g�I�p�̍S������
	if ($config_test && $in{wt_refresh}) {
		$m{wt} = 0;
	}
	# �ȉ��ʏ�̍S�������
	elsif ($is_mobile && $m{lib_r} eq '') {
		my $next_time_mes = sprintf("���ɍs���ł���܂� %d��%02d�b<br>", int($m{wt} / 60), int($m{wt} % 60) );
		$mes .= &disp_now();
		$mes .= $next_time_mes;
	}
	elsif($is_smart && $m{lib_r} eq '') {
		my $next_time_mes = sprintf("%d��%02d�b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("��<b>%d</b>��<b>%02d</b>����", $nokori_time / 3600, $nokori_time % 3600 / 60);
		$mes .= &disp_now();
		$mes .= qq|\n���ɍs���ł���܂� <span id="nokori_time">$next_time_mes</span>\n|;
		$mes .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$mes .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$mes .= qq|�G��[�O��F<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> �A��<b>$m{renzoku_c}</b>��]<br>| if $m{renzoku_c};
		$mes .= qq|���̋����܂� $nokori_time_mes|;
	}
	elsif ($m{lib_r} eq '') {
		my $head_mes = '';
		if (-f "$userdir/$id/letter_flag.cgi") {
			open my $fh, "< $userdir/$id/letter_flag.cgi";
			my $line = <$fh>;
			my($letters) = split /<>/, $line;
			close $fh;
			$main_screen .= qq|<font color="#FFCC66">�莆�� $letters ���͂��Ă��܂�</font><br>| if $letters;
#			$main_screen .= qq|<font color="#FFCC66">�莆���͂��Ă��܂�</font><br>|;
		}
		if (-f "$userdir/$id/depot_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC00">�a���菊�ɉו����͂��Ă��܂�</font><br>|;
		}
		if (-f "$userdir/$id/goods_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC99">ϲٰтɉו����͂��Ă��܂�</font><br>|;
		}
		my $is_breeder_find = 0;
		for my $bi (0 .. 2) {
			if (-f "$userdir/$id/shopping_breeder_$bi.cgi") {
				if ((stat "$userdir/$id/shopping_breeder_$bi.cgi")[9] < $time) {
					$is_breeder_find = 1;
				}
			}
		}
		$main_screen .= qq|<font color="#FF66CC">��ĉ��̗����z�����Ă��܂�</font><br>| if $is_breeder_find;
		my $next_time_mes = sprintf("%d��%02d�b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("��<b>%d</b>��<b>%02d</b>����", $nokori_time / 3600, $nokori_time % 3600 / 60);

		$main_screen .= &disp_now();

		$main_screen .= qq|\n���ɍs���ł���܂� <span id="nokori_time">$next_time_mes</span>\n|;
		$main_screen .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$main_screen .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$main_screen .= qq|�G��[�O��F<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> �A��<b>$m{renzoku_c}</b>��]<br>| if $m{renzoku_c};
		$main_screen .= qq|���̋����܂� $nokori_time_mes<br><br>|;

		require "$datadir/twitter_bots.cgi";
		$main_screen .= &{$twitter_bots[6]};
	}
#	$menu_cmd .= qq|<form method="$method" action="bj_rest_shop.cgi">|;
#	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="pass" value="$pass">|;
#	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="�X�ɍs��" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="�X�ɍs��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

	# �S�����ɍs�����ĂȂ�
	unless ($m{lib_r}) {
		&n_menu;
		&menu( map { $_->[0] } @menus );
	}

	if ($config_test) {
		$menu_cmd .= qq|<form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="wt_refresh" value="1">|;
		$menu_cmd .= $is_mobile ? qq|<input type="submit" value="�S������" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="�S������" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}
}
else {
	if (-f "./lib/$m{lib}.cgi") { # lib �Ăяo��
		if ($m{tp} eq '1' && $cmd eq '0') { # begin�ƭ���0(��߂�)��I������ݾ�
			if ($m{lib} =~ /shopping_/) {
				require './lib/shopping.cgi';
				&refresh;
				$m{lib} = 'shopping';
			}
			else {
				$mes .= '��߂܂���<br>';
				require './lib/main.cgi';
				&refresh;
			}
		}
		else {
			require "./lib/$m{lib}.cgi";
		}
	}
	else { # ��̫��lib �Ăяo��
		require './lib/main.cgi';
	}
	
	if ($m{tp}) { # lib ����
		&{ 'tp_'.$m{tp} } if &is_satisfy; # is_satisfy��1(true)�Ȃ珈������
	}
	else { # begin �ƭ�
		$m{tp} = 1;
		&begin;
	}
}
&auto_heal unless $is_battle;
$is_mobile ? require './lib/template_mobile_base.cgi' :
	$is_smart ? require './lib/template_smart_base.cgi' :
	$is_appli ? require './lib/template_appli_base.cgi' : require './lib/template_pc_base.cgi';
&write_user;
&footer;
# ------------------
# ���Ԃɂ���
sub auto_heal {
	my $v = $time - $m{ltime}; 
	$v = &use_pet('heal_up', $v);
	$v = int( $v / $heal_time ); 
	$m{hp} += $v;
	$m{mp} += int($v * 0.8);
	$m{hp} = $m{max_hp} if $m{hp} > $m{max_hp};
	$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
}

sub disp_now {
	my $state = "���̑�";
	if($m{lib} eq 'domestic'){
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "�_�ƒ��ł�";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "���ƒ��ł�";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "�������ł�";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}elsif($m{turn} eq '4'){
				$state = "���K��";
			}else{
				$state = "���K��";
			}
			$state .= "�����������ł�";
		}
	}elsif($m{lib} eq 'military'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{tp} eq '110'){
			$state .= "(���D)";
		}elsif($m{tp} eq '210'){
			$state .= "(����)";
		}elsif($m{tp} eq '310'){
			$state .= "(���])";
		}elsif($m{tp} eq '410'){
			$state .= "(��@)";
		}elsif($m{tp} eq '510'){
			$state .= "(�U�v)";
		}elsif($m{tp} eq '610'){
			$state .= "(�U��)";
		}elsif($m{tp} eq '710'){
			if($m{value} eq 'military_ambush'){
				$state = "�R��";
			}else{
				$state = "�i�R";
			}
			$state .= "�҂��������ł�";
		}elsif($m{tp} eq '810'){
			$state .= "(�������D)";
		}elsif($m{tp} eq '910'){
			$state .= "(��������)";
		}elsif($m{tp} eq '1010'){
			$state .= "(�������])";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{name}[$y{country}]��$cs{prison_name}[$y{country}]�ŗH���ł�";
	}elsif($m{lib} eq 'promise'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{tp} eq '110'){
			$state .= "(�F�D)";
		}elsif($m{tp} eq '210'){
			$state .= "(���)";
		}elsif($m{tp} eq '310'){
			$state .= "(���z��)";
		}elsif($m{tp} eq '410'){
			$state .= "(��������)";
		}elsif($m{tp} eq '510'){
			$state .= "(�����j��)";
		}elsif($m{tp} eq '610'){
			$state = "�������ֈړ����ł�(�H���A��)";
		}elsif($m{tp} eq '710'){
			$state = "�������ֈړ����ł�(�����A��)";
		}elsif($m{tp} eq '810'){
			$state = "�������ֈړ����ł�(���m�A��)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{value} eq '0.5'){
			$state .= "(�����i�R)";
		}elsif($m{value} eq '1'){
			$state .= "(�i�R)";
		}elsif($m{value} eq '1.5'){
			$state .= "(��������)";
		}
	}
	return "$state<br>\n";
}

1; # �폜�s�� login.cgi�� bj.cgi��require���Ă���
