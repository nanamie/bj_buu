#================================================
# 祭り情勢の開始・終了で使われるモジュール
#================================================

#================================================
# 主な呼び出し元
# ./lib/_world_reset.cgi
# 自動的に呼ばれるので意識してロードする必要はない
#================================================

# 祭り情勢の開始と終了に紐づくので 1 ずつ空ける
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# 祭り情勢の名称と、開始時なら 1 終了時 なら 0 を指定する
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

1;