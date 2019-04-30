from web_app.spotify_methods import clear_tracks_csv, write_tracks_to_csv, prompt_token_flask

#file placed in main app directory so that these functions may be tested as written
def test_clear_csv():
	#checks to see if the csv clear function works
	result = clear_tracks_csv()
	assert result == True


def test_write_to_csv():
	#tests to make sure if the csv writing function works
	test = ['test']
	result = write_tracks_to_csv(test)
	clear_tracks_csv
	assert result == True


def test_prompt_token_flask():
	#checks to make sure a spotify oauth object is created
	result = prompt_token_flask("gmr0678")
	if result is not None:
		result_valid = True

	assert result_valid == True
