#アクセッサーのテスト

package TestAccessor;

use feature 'say';
use lib qw(./TestFramework/Controller/Accessor);
require "CountryAccessor.pm";
require "WorldAccessor.pm";
require "WarAccessor.pm";
require "PlayerAccessor.pm";
require "ItemAccessor.pm";

my $username_first_part = "test";
my $username_sufix = "28";
my $username = $username_first_part.$username_sufix;
my $user_id = unpack ('H*', $username);
my $passward = "test4a";
my $first_country = 2;
my $second_country = 3;
my $added_country_name = "test_country";

#test_ca();
test_pa();
#test_wa();
#taihi();
#test_wara();
#test_ia();

sub taihi{
	my $pa =  PlayerAccessor->new();
	$pa->access_data($username, "wt", 0);
	$pa->access_data($username, "tp", 0);
	$pa->access_data($username, "lib", "");
	$pa->access_data($username, "lea", 999);
	$pa->access_data($username, "cha", 999);
	$pa->access_data($username, "act", 0);
	$pa->access_data($username, "renzoku_c", 0);
	$pa->access_data($username, "ag", 999);
}

#PlayerAccessorテスト
sub test_pa{
	
	print "***test_pa::start***\n\n";

	my $pa = PlayerAccessor->new();
	my $ca = CountryAccessor->new();

	#プレイヤー作成 成功
	print "test1\n";
	$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	print "test2\n";
	unless ($pa->access_data($username, "hp")){
		die("create_player success");
	}

	

	#プレイヤー士官 失敗　
	#存在しない国番号
	print "********p1**********\n";
	eval{
		$pa->access_data($username, "wt", 0);
		$pa->access_data($username, "tp", 1);
		$pa->access_data($username, "lib", "");
		$pa->shikan_player($username, 999);
	};
	unless($@){
		die("shikan_player fail 1 $@");
	}
	
	#プレイヤー士官 失敗　
	#拘束中
	print "********p2**********\n";
	$pa->access_data($username, "wt", 100);
	$pa->access_data($username, "tp", 1);
	$pa->access_data($username, "lib", "");
	eval{
		$pa->shikan_player($username, $first_country);
	};
	unless ($@) {
		die("shikan_player fail 2");
	}
	
	#プレイヤー士官　失敗
	#投獄中
	
	#プレイヤー士官　失敗
	#士官出来ない情勢
	
	#プレイヤー士官　失敗
	#士官上限

	#プレイヤー士官　成功
	
	print "********p3**********\n";
	$ca->access_data($first_country, "capacity", 30);
	$pa->access_data($username, "wt", 0);
	$pa->access_data($username, "tp", 1);
	$pa->access_data($username, "lib", "");
	$pa->shikan_player($username, $first_country);
	if($pa->access_data($username, "country") ne $first_country){
		die("shika_player success");
	}

	#プレイヤー削除　成功
	print "********p4**********\n";
	$pa->remove_player($username);
	eval{
		$pa->access_data($username, "act", 10);
	};
	unless ($@) {
		die("remove_player success");
	}

	print "********p5**********\n";
	#プレイヤー削除　失敗
	#存在しないプレイヤー
	eval{
		$pa->remove_country("kakuu");
	};
	unless ($@) {
		die("remove_player fail");
	}



	print "\n***test_pa::end***\n\n";
}

#CountryAccessorテスト
sub test_ca{

	print "***test_ca::start***\n\n";
	my $ca = CountryAccessor->new();

	#access_data
	say "*** access_data test ***";
	say "capacity of country 1 = ", $ca->access_data(1, "capacity") ;
	say "set 35 to capacity of country 1 = ", $ca->access_data(1, "capacity", 35);
	say "capacity of country 1 = ", $ca->access_data(1, "capacity");

	#add_country
	say "*** add_country test***";
	say "num_country = ", $ca->get_num_country();
	my $added_country = $ca->add_country($added_country_name, "#000FFF");
	say "num_country = ", $ca->get_num_country();

	#remove_country 
	#say "*** remove_country test***";
	#$ca->remove_country($added_country);
	#say "num_country = ", $ca->get_num_country();
	print "\n***test_ca::end***\n\n";
}

#WorldAccesorテスト
sub test_wa{

	print "***test_wa::start***\n\n";
	my $wa = WorldAccessor->new();

	#国の数
	my $year = $wa->access_data("country", 6);
	my $year = $wa->access_data("year");
	say "year = ", $year; 
	$wa->access_data("year", 13);	
	say "year = ", $wa->access_data("year");
	$wa->access_data("year", 15);	
	
	#災害起こす
	$wa->evoke_disaster();
	$wa->evoke_disaster(1);
	print "***test_wa::end***\n\n";
}

#WarAccessorテスト
sub test_wara{

	print "***test_wara::start***\n\n";
	my $pa = PlayerAccessor->new();
	my $wara = WarAccessor->new();
	my $ca = CountryAccessor->new();
	my $wa = WorldAccessor->new();

	#$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	#$ca->access_data($first_country, "capacity", 25);
	#print $pa->shikan_player($username, $first_country);
	$pa->access_data($username, "wt", 0);
	$pa->access_data($username, "act", 0);
	$pa->access_data($username, "tp", 0);
	$pa->access_data($username, "lib", "");
	$ca->access_data($first_country, "food", 100000);
	$ca->access_data($first_country, "money", 100000);
	$ca->access_data($first_country, "soldier", 100000);
	
	#set_war success
	print "*****enter set_war success*********\n";
	$wa->access_data("reset_time", 0);
	$wara->set_war($username, $second_country,1);
	my $res = $pa->access_data($username, "lib");
	if($res ne "war"){
		die($testname."set_war success test : \$res = $res".$mes);
	}


	#set_war fail
	#期待：既に直前にset_warしているから失敗
	print "*****enter set_war fail*********\n";
	eval{
		$wara->set_war($username, $second_country, 1);
	};
	if($@){
	}
	else{
		die($testname."set_war fail test");
	
	}
	
	#encount fail
	#期待：拘束中のはず
	print "*****enter encount fail*********\n";
	eval{
		$wara->encount($username);
	};
	if($@){
	}
	else{
		die($testname."encount fail test");
	}

	
	#encount success
	print "*****enter encount success*********\n";
	$pa->access_data($username, "wt", 0);
	$wara->encount($username);
	my $lib = $pa->access_data($username, "lib");
	if ($lib ne "war"){
		die("encount success test: lib = $lib");		
	}

	

	#step_war success
	print "*****enter encount success*********\n";
	$sum_c = $pa->access_data($username, "lose_c")
	       + $pa->access_data($username, "win_c")
	       + $pa->access_data($username, "draw_c");

	while(1){
		$wara->step_war($username);
		if($pa->access_data($username, "tp") eq 0) {return 1;}
	};

	$new_sum_c =  $pa->access_data($username, "lose_c")
	       + $pa->access_data($username, "win_c")
	       + $pa->access_data($username, "draw_c");

	unless ($sum_c lt $new_sum_c){
		die("step_war success");
	}

	$pa->remove_player($username);



	print "***test_wara::end***\n\n";
}

sub test_ia{

	print "***test_ia start***\n\n";
	my $pa = PlayerAccessor->new();
	my $wara = WarAccessor->new();
	my $ca = CountryAccessor->new();
	my $wa = WorldAccessor->new();
	my $ia = ItemAccessor->new();

	$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	$ca->access_data($first_country, "capacity", 25);
	print $pa->shikan_player($username, $first_country);

	my $new_wepon = [1, 1, 15, 4];
	my $new_egg = [2, 10, 10, 0];
	my $new_pet = [3, 61, 1, 0];
	my $new_gar = [4, 1, 0, 0];

	$ia->give_item($username, $new_wepon->[0], $new_wepon->[1], $new_wepon->[2], $new_wepon->[3]);
	$ia->give_item($username, $new_egg->[0], $new_egg->[1], $new_egg->[2], $new_egg->[3]);
	$ia->give_item($username, $new_pet->[0], $new_pet->[1], $new_pet->[2], $new_pet->[3]);
	$ia->give_item($username, $new_gar->[0], $new_gar->[1], $new_gar->[2], $new_gar->[3]);

	my $wep_index = $ia->get_item_index($username, $new_wepon->[0], $new_wepon->[1], $new_wepon->[2], $new_wepon->[3]);
	my $egg_index = $ia->get_item_index($username, $new_egg->[0], $new_egg->[1], $new_egg->[2], $new_egg->[3]);
	my $pet_index = $ia->get_item_index($username, $new_pet->[0], $new_pet->[1], $new_pet->[2], $new_pet->[3]);
	my $gar_index = $ia->get_item_index($username, $new_gar->[0], $new_gar->[1], $new_gar->[2], $new_gar->[3]);

	die("index does not match : expected 0: actual $wep_index") if($wep_index ne 0);
	die("index does not match : expected 1: actual $egg_index") if($egg_index ne 1);
	die("index does not match : expected 2: actual $pet_index") if($pet_index ne 2);
	die("index does not match : expected 3: actual $gar_index") if($gar_index ne 3);

	$ia->draw_item($username, 0);
	$ia->draw_item($username, 0);
	$ia->draw_item($username, 0);
	$ia->draw_item($username, 0);
	$ia->draw_item($username, $pet_index);
	
	unless( ($pa->access_data($username, "wea") eq $new_wepon->[1])
		and ($pa->access_data($username, "wea_c") eq $new_wepon->[2])
		and ($pa->access_data($username, "wea_lv") eq $new_wepon->[3])
		and ($pa->access_data($username, "egg") eq $new_egg->[1])
		and ($pa->access_data($username, "egg_c") eq $new_egg->[2])
		and ($pa->access_data($username, "pet") eq $new_pet->[1])
		and ($pa->access_data($username, "pet_c") eq $new_pet->[2])
		and ($pa->access_data($username, "gua") eq $new_gar->[1])){
	
		die("draw_item didn't work properly");
	}

	#ｱﾏﾂﾐ使用
	my $pet_effect = $ia->use_pet($username);
	die("use_pet didn't work : pet_effect expected 0 : acutual $pet_effect") if ($pet_effect ne 0);



	print "***test_ia end***\n\n";

}
