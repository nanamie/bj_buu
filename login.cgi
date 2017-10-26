#!/usr/local/bin/perl --
use Time::HiRes;
$load_time = Time::HiRes::time unless $load_time;
require './lib/system.cgi';
require './lib/move_player.cgi';
use File::Copy;
#================================================
# ��ڲ԰�ꗗHTML�쐬 + �����؂���ڲ԰�폜
# & Cookie���(PC�̂�) Created by Merino
#================================================

# ��ڲ԰�ꗗHTML�X�V����(��) 1���`
my $update_cycle_day = 1;

# Cookie�ۑ�����(��)
my $limit_cookie_day = 30;


#================================================
&decode;
$in{is_cookie} ? &set_cookie($in{login_name},$in{pass},1) : &del_cookie unless $is_mobile;
require 'bj.cgi';

# ����҂����ꂸ
if ($time > $w{limit_time}) {
	require './lib/reset.cgi';
	&time_limit;
}

#&summary_contribute;

# htmļ�ٍ쐬 & �����؂���ڲ԰�폜
for my $i (0 .. $w{country}) {
	if (-M "./html/$i.html" >= $update_cycle_day) {
#	if (-M "./html/$i.html" >= 0) {
		&write_players_html($i);
		last;
	}
}

my $chart_time = (stat "./html/chart_img.html")[9];
if($chart_time < $time - 3600){
	&chart_backup;
}

if (-M "./html/all.html" >= $update_cycle_day) {
#if (-M "./html/$i.html" >= 0) {
	&write_all_players_html;
	&backup_players;
}
#&make_player_name_list;
#&refresh_new_commer;

exit;

#=================================================
# �������
#=================================================
sub set_cookie {
	my @cooks = @_;

	local($csec,$cmin,$chour,$cmday,$cmon,$cyear,$cwday) = gmtime(time + $limit_cookie_day * 24 * 60 * 60); # 24���� * 60�� * 60�b
	local @mons = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	local @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	local $expirese_time = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$cwday],$cmday,$mons[$cmon],$cyear+1900,$chour,$cmin,$csec);

	for my $c (@cooks) {
		$c =~ s/(\W)/sprintf("%%%02X", unpack "C", $1)/eg;
		$cook .= "$c<>";
	}

	print "Set-Cookie: bj=$cook; expires=$expirese_time\n";
}

# ------------------
# �����폜
sub del_cookie {
	my $expires_time = 'Thu, 01-Jan-1970 00:00:00 GMT';
	print "Set-Cookie: bj=dummy; expires=$expires_time\n";
}


#=================================================
# �����Ƃ�htmļ�ٍ쐬
#=================================================
# �\�����鍀�ڂ𑝌�����ꍇ�́A@rows �� 130�s�ڎ��ӂ�ҏW���Ă�

sub write_players_html {
	my $country = shift;

	my @rows = (qw/���O ���� �K�� ���� �E�� �푰 ���� �Ϻ� �߯� ���� Lv HP MP AT DF MAT MDF AG LEA CHA ���� ��� �X�V���� ү���� �Q������/);

	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;

	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	open my $fh, "< $logdir/$country/member.cgi";
	while (my $player = <$fh>) {
		$player =~ tr/\x0D\x0A//d;
		
		# �������O�̐l����������ꍇ
		next if ++$sames{$player} > 1;

		my $player_id = unpack 'H*', $player;

		# ���݂��Ȃ��ꍇ��ؽĂ���폜
		unless (-f "$userdir/$player_id/user.cgi") {
			&move_player($player, $country, 'del');
			next;
		}

		my %p = &get_you_datas($player_id, 1);
		
		# �폜�����ɂȂ莩���폜
		if ($time > $p{ltime} + $auto_delete_day * 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			# �����폜�����߯Ă𑕔����Ă���Ȃ玩���폜���{30���͍폜���Ȃ�
			if ($pets[$p{pet}][2] eq 'life_up') {
				if ($time > $p{ltime} + ($auto_delete_day + 30) * 3600 * 24) {
					&move_player($player, $country, 'del');
					next;
				}
			}
			else {
				&move_player($player, $country, 'del');
				next;
			}
		}
		# �׌������̐l(�P����ڂ̃��x���P)���T���ڂō폜
		elsif ($p{lv} <= 1 && $p{sedai} <= 1 && $time > $p{ltime} + 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			&move_player($player, $country, 'del');
			next;
		}
		# �޸ނȂǂňႤ���̐l���������Ă���ꍇ
		elsif ($p{country} ne $country) {
			&move_player($player, $country, $p{country});
			next;
		}
		
		my $name = $p{name};
		$name .= "[$p{shogo}]" if $p{shogo};
		
		my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..5];
		my $start_date = sprintf("%d/%d/%d %02d:%02d", $year+1900, $mon+1, $mday, $hour, $min);

#		$html .= $count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
		my $rank_name = &get_rank_name($p{rank}, $p{name});
		$html .= qq|<tr>|;
		$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
		$html .= qq|<td>$sexes[$p{sex}]</td>|;
		$html .= qq|<td>$rank_name</td>|;
		$html .= qq|<td>$units[$p{unit}][1]</td>|;
		$html .= qq|<td>$jobs[$p{job}][1]</td>|;
		$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
		$html .= qq|<td>$weas[$p{wea}][1]</td>|;
		$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
		$html .= qq|<td>$pets[$p{pet}][1]</td>|;
		$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
		$html .= qq|<td>$p{ldate}</td>|;
		$html .= qq|<td>$p{mes}</td>|;
		$html .= qq|<td>$start_date</td>|;
		$html .= qq|</tr>\n|;
		
		# ���v
		++$ranks{$p{rank}};
		++$weas{$weas[$p{wea}][2]};
		++$jobs{$p{job}};
		++$_seeds{$p{seed}};
		++$sexes{$p{sex}};
		++$units{$p{unit}};
		++$count;
	}
	close $fh;
	$html .= qq|</tbody></table>|;
	
	# �����l���␳
	$cs{member}[$country] = $count;

	if ($country eq '1') {
		$w{playing} = int($w{playing} * 0.9); # �S�����炸������l���l�����ď������炷
	}

	&write_cs if $country > 0;

	# ���vHTML
	my $html_chart  = $w{world} eq $#world_states && $country eq $w{country} ? qq|<hr size="1"><h1>$cs{name}[$country] �̈����B</h1>| : qq|<hr size="1"><h1>$cs{name}[$country] �̗E�m�B</h1>|;
	   $html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>�����l��</th><td>$count�l|;

	$html_chart .= qq|<br></td></tr><tr><th>����</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}�l/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�K��</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>����</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>���푮��</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�E��</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�푰</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}
	
	$html_chart .= qq|<br></td></tr></table><br>|;
	
	# HTMĻ�ٍ쐬
	open my $out, "> ./html/$country.html";
	print $out &header_players_html($country);
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;
	
	# �g�їp�ɓ��vHTML�o��
	open my $out2, "> ./html/${country}_chart.html";
	print $out2 &header_chart_html($country);
	print $out2 $html_chart;
	print $out2 &footer_players_html;
	close $out2;
}

sub write_all_players_html {
	my @rows = (qw/���O ���� �K�� ���� �E�� �푰 ���� �Ϻ� �߯� ���� Lv HP MP AT DF MAT MDF AG LEA CHA ���� ��� �X�V���� ү���� �Q������/);
	
	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;
	
	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	for my $country (0..$w{country}){
		open my $fh, "< $logdir/$country/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;

			# �������O�̐l����������ꍇ
			next if ++$sames{$player} > 1;

			my $player_id = unpack 'H*', $player;


			my %p = &get_you_datas($player_id, 1);

			my $name = $p{name};
			$name .= "[$p{shogo}]" if $p{shogo};
		
			my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..5];
			my $start_date = sprintf("%d/%d/%d %02d:%02d", $year+1900, $mon+1, $mday, $hour, $min);

			my $rank_name = &get_rank_name($p{rank}, $p{name});
			$html .= qq|<tr>|;
			$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
			$html .= qq|<td>$sexes[$p{sex}]</td>|;
			$html .= qq|<td>$rank_name</td>|;
			$html .= qq|<td>$units[$p{unit}][1]</td>|;
			$html .= qq|<td>$jobs[$p{job}][1]</td>|;
			$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
			$html .= qq|<td>$weas[$p{wea}][1]</td>|;
			$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
			$html .= qq|<td>$pets[$p{pet}][1]</td>|;
			$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
			$html .= qq|<td>$p{ldate}</td>|;
			$html .= qq|<td>$p{mes}</td>|;
			$html .= qq|<td>$start_date</td>|;
			$html .= qq|</tr>\n|;

			# ���v
			++$ranks{$p{rank}};
			++$weas{$weas[$p{wea}][2]};
			++$jobs{$p{job}};
			++$_seeds{$p{seed}};
			++$sexes{$p{sex}};
			++$units{$p{unit}};
			++$count;
		}
		close $fh;
	}
	$html .= qq|</tbody></table>|;

	# ���vHTML
	my $html_chart  = qq|<hr size="1"><h1>�S���̗E�m�B</h1>|;
	$html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>�����l��</th><td>$count�l|;

	$html_chart .= qq|<br></td></tr><tr><th>����</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}�l/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�K��</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>����</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>���푮��</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�E��</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>�푰</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}
	
	$html_chart .= qq|<br></td></tr></table><br>|;
	
	# HTMĻ�ٍ쐬
	open my $out, "> ./html/all.html";
	print $out &header_all_players_html;
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;

}

# ------------------
sub header_players_html {
	my $country = shift;

my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / $cs{name}[$country]</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="�s�n�o" class="button1"></form>
<p>�X�V���� $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= $i eq $country
			? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / |
			: qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |
			;
	}
	
	$html .= qq|<a href="all.html"><font color="#ffffff">�S�v���C���[</font></a> / |;
	
	if ($is_backup_countries) {
		$html .= $country eq 'chart' ? qq|�������� / | : qq|<a href="chart_img.html">��������</a> / |;
	}
	
	return $html;
}

sub header_all_players_html {
my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / �S�v���C���[</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="�s�n�o" class="button1"></form>
<p>�X�V���� $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |;
	}
	
	$html .= qq|<font color="#ffffff">�S�v���C���[</font> / |;
	
	if ($is_backup_countries) {
		$html .= qq|<a href="chart_img.html">��������</a> / |;
	}
	
	return $html;
}
# ------------------
sub chart_backup {
	# �ޯ����ߏ���
	if ($is_backup_countries && -d "./backup" && -s "$logdir/countries.cgi" > 300) {
		my @lines = ();
		open my $fh_b, "< $logdir/countries.cgi";
		while (my $line = <$fh_b>) {
			push @lines, $line;
		}
		close $fh_b;
		
		my($mhour,$wday) = (localtime($time))[2,6];
		my $hour_file = "./backup/" . $wday . "_" . $mhour . ".cgi";
		open my $fh_b2, "> $hour_file";
		print $fh_b2 @lines;
		close $fh_b2;
		
		my $del_start = $wday + 1;
		my $del_end = $wday + 6;
		
		for my $d ($del_start..$del_end){
			my $del_d = $d > 6 ? $d - 7 : $d;
			for my $h (0..23){
				my $hour_file = "./backup/" . $del_d . "_" . $h . ".cgi";
				if(-f "$hour_file"){
					unlink $hour_file;
				}
			}
		}
		
		&create_world_chart;
	}
}

sub header_chart_html {
	my $country = shift;

	my $html = '';
	$html .= qq|<html><head>|;
	$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	$html .= qq|<title>$title / $cs{name}[$country]</title>|;
	$html .= qq|</head><body $body>|;
	$html .= qq|<form method="$method" action="../$script_index"><input type="submit" value="�s�n�o"></form>|;
	$html .= qq|<form method="$method" action="../players.cgi"><input type="submit" value="�߂�"></form>|;
	$html .= qq|<p>�X�V���� $date</p>|;
	$html .= qq|<hr size="1"><h1>$cs{name}[$country]</h1>|;
	
	return $html;
}
# ------------------
sub footer_players_html {
	my $html = '';
	$html .= qq|<br><div align="right" style="font-size:11px">|;
	$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama�y.net</a><br>|;  # ����\��:�폜�E��\�� �֎~!!
	$html .= qq|$copyright|;
	$html .= qq|</div></body></html>|;

	return $html;
}

# �ޯ����߂���ް����擾
sub create_world_chart {
	$touitu_strong = 0 if ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10')); # ���E�[�[��]
	
	# �ޯ�����̧�ق��Â����̏��ɿ��
	my @lines = ();
	opendir my $dh, "backup";
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		
		my $file_time = (stat "./backup/$file_name")[9];
		push @lines, "$file_name<>$file_time<>\n";
	}
	closedir $dh;

	@lines = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ]} @lines;
	
	# ���͂��擾
	my $chxl_x = '';
	my @chds = ();
	my $count_day = 0;
	for my $line (@lines) {
		my($file_name, $file_time) = split /<>/, $line;
		
		my $i = 1;
		open my $fh, "< ./backup/$file_name";
		my $head_line = <$fh>;
		while (my $data_line = <$fh>) {
			if ($data_line =~ /<>is_die;1<>/) {
				$chds[$i] .= "0,";
			}
			else {
				my($strong)    = ($data_line =~ /<>strong;(\d+?)<>/);
				my $strong_par = $strong <= 0 || $touitu_strong <= 0 ? 0 : int($strong / $touitu_strong * 100);
				$strong_par = 100 if $strong_par > 100;
				$chds[$i] .= "$strong_par,";
			}
			++$i;
		}
		close $fh;
		
		my($mhour,$mday,$month) = (localtime($file_time))[2,3,4];
		++$month;
		$chxl_x .= "|$month/$mday $mhour:00";
		
		++$count_day;
	}
	my $chg_x = $count_day <= 2 ? 25 : int(50 / ($count_day-1) * 100) * 0.01;
	
	my $name = '';
	my $chco = '';
	my $chd = '';
	for my $i (1 .. $w{country}) {
		$chco .= "$cs{color}[$i],";
		chop $chds[$i]; # �����,���Ƃ�
		$chd  .= "$chds[$i]|";
		
		$name .= qq|<font color="$cs{color}[$i]">���y ���� <b>$cs{win_c}[$i]</b> �z$cs{name}[$i]</font><br>|;
	}
	$chco =~ tr/#//d; # #������
	chop $chco; # �����,���Ƃ�
	chop $chd;  # �����|���Ƃ�
	
	my $one_tenth = int($touitu_strong * 0.1);
	my $count_scale = 0;
	my $scale = 0;
	my $chxl_y = '';
	for my $i (1 .. 15) {
		$chxl_y .= "|$scale";
		$scale += int($one_tenth * 0.01) * 100;
		++$count_scale;
		last if $scale >= $touitu_strong*0.95;
	}
	$chxl_y .= "|$touitu_strong";
	$chg_y = $count_scale <= 0 ? 25 : int(100 / $count_scale * 100) * 0.01;
	
	my $html = qq|<hr size="1"><h1>$world_name�嗤��������</h1>|;
	$html .= qq{<img src="http://chart.apis.google.com/chart?cht=lc&chs=500x350&chco=$chco}
		  .  qq{&chd=t:$chd&chxt=x,y,r&chxl=0:$chxl_x|1:$chxl_y|2:|Die|Harf|Win}
		  .  qq{&chg=$chg_x,$chg_y&chtt=World+Force+Chart&chf=c,lg,110,003366,0.7,000000,0|bg,s,CCCCCC">};

	my $limit_day = int( ($w{limit_time} - $time) / (3600 * 24) );
	$html .= qq|<p>$name</p>|;
	$html .= qq|$world_name��y $w{year}�N �z/ ���E��y $world_states[$w{world}] �z/ ��������y �c��$limit_day�� �z/<br>|;
	$html .= qq|��Փx�y Lv.$w{game_lv} �z/ ����$e2j{strong}�y $touitu_strong �z/ | unless ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10'));

	my($c1, $c2) = split /,/, $w{win_countries};
	$html .= $c2 ? qq|���ꍑ�y <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>���� �z<br>|
		   : $c1 ? qq|���ꍑ�y <font color="$cs{color}[$c1]">$cs{name}[$c1]</font> �z<br>|
		   :       qq|<br>|
		   ;
	
	# HTMĻ�ٍ쐬
	open my $out, "> ./html/chart_img.html";
	print $out &header_players_html('chart');
	print $out $html;
	print $out &footer_players_html;
	close $out;
}

sub backup_players {
	mkdir "./snap_shot/snap_shot_$time";
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my $user_from = "$userdir/$pid/user.cgi";
		my $user_to = "./snap_shot/snap_shot_$time/user_$pid.cgi";
		
		copy($user_from, $user_to);
	}
	closedir $dh;
	
	my $countries_from = "$logdir/countries.cgi";
	my $countries_to = "./snap_shot/snap_shot_$time/countries.cgi";
	copy($countries_from, $countries_to);
	
	opendir my $rdh, "./snap_shot" or &error("�ޯ������ިڸ�؂��J���܂���");
	while (my $backup_name = readdir $rdh) {
		if ($backup_name =~ /snap_shot_(\d+)/) {
			if ($1 < $time - 3 * 24 * 60 * 60) {
				rmtree(["./snap_shot/$backup_name"]);
			}
		}
	}
	closedir $rdh;
}
