#TestFramework/Situations/situation1.pmで生成されるデータをロードする
package refresh_situation1;

&run;

sub run{
	use TestFramework::Controller::ControllerConst;
	
	require  $ControllerConst::situation_loader;
	SituationLoader::load_situation("situation1");
}
1;
