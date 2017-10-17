#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# ƭ���\�� Created by Merino
#================================================

# �\���������(./log/�ɂ������)�@�ǉ��폜���בւ��\
my @files = (
#	['����',		'۸�̧�ٖ�'],
	['�ߋ��̉h��',	'world_news',		],
	['���E�',	'world_big_news',	],
	['�������',	'send_news',		],
	['���Z��̋O��','colosseum_news',	],
	['�V����۸�',	'blog_news',		],
	['�V��G��',	'picture_news',		],
	['�V��{',		'book_news',		],
	['�Q�����O',	'entry_news',		],
);

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	if ($in{id} && $in{pass}) {
		if ($is_appli) {
			&show_page_switcher;
		}
		else {
			print qq|<div style="margin-bottom: 14px;">|;
			print qq|<form method="$method" action="$script" style="display: inline;">|;
			print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
			print qq|<input type="submit" value="�߂�" class="button1"></form>|;
			&show_wait;
			print qq|</div>|;
		}
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="�s�n�o" class="button1"></form>|;
	}
	
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="./amida.cgi?id=$in{id}&pass=$in{pass}">���޸��</a> / |;

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	print qq|<font size="1">���摜���\\������Ă��Ȃ����̂́A���̐l��ϲ�߸������Ȃ��Ȃ������̂ł�</font><br>| if $files[$in{no}][1] eq 'picture_news';
	
	open my $fh, "< $logdir/$files[$in{no}][1].cgi" or &error("$logdir/$files[$in{no}][1].cgi̧�ق��ǂݍ��߂܂���");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}

sub show_wait {
	&read_user;
#	my %p = get_you_datas($in{id}, 1);
	my $state = '';
	if ($m{lib} eq 'domestic') {
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
		$state = "�ړ����ł�";
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
		$state = "$cs{prison_name}[$y{country}]�ŗH���ł�";
	}elsif($m{lib} eq 'promise'){
		$state = "�ړ����ł�";
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
			$state .= "(�H���A��)";
		}elsif($m{tp} eq '710'){
			$state .= "(�����A��)";
		}elsif($m{tp} eq '810'){
			$state .= "(���m�A��)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "�ړ����ł�";
		if($m{value} eq '0.5'){
			$state .= "(�����i�R)";
		}elsif($m{value} eq '1'){
			$state .= "(�i�R)";
		}elsif($m{value} eq '1.5'){
			$state .= "(��������)";
		}
	}

	if ($state) {
		my $next_time_mes = sprintf("%d��%02d�b", int($m{wt} / 60), int($m{wt} % 60) );
		print qq| $state|;
		print qq| <span id="nokori_time">$next_time_mes</span>| if 0 < $m{wt};
	}
}
