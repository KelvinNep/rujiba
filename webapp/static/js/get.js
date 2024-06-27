$(document).ready(function() {
    $(document).on('click', '.btnaddjurnal', function(e) {
        const selectRegu = $('#id_regu');
        selectRegu.empty(); 
		selectRegu.append('<option disabled selected>Select Regu</option>');
		
        $.ajax({
            url: '/get_survey/',
            method: 'GET',
            success: function(data) {
                if (data.length === 0) {
                    selectRegu.append('<option value="">No surveys available</option>');
                } else {
                    data.forEach(survey => {
                        selectRegu.append(`<option value="${survey.id}">${survey.nama}</option>`);
                    });
                }
            },
            error: function(error) {
                console.error('Error fetching survey data:', error);
                selectRegu.append('<option value="">Error fetching data</option>');
            }
        });
    });


	$(document).on('click', '.edit-jurnal', function(e) {
		var jurnalId = $(this).data('id');
        const selectRegu = $('#edit_id_regu');
        selectRegu.empty(); 

        $.ajax({
			url: '/get_survey/',
			method: 'GET',
			success: function(data) {
				if (data.length === 0) {
					selectRegu.append('<option value="">No surveys available</option>');
				} else {
					// Ambil data jurnal yang sedang diedit
					$.ajax({
						type: 'GET',
						url: '/edit_jurnal/' + jurnalId + '/',
						success: function(jurnalData) {
							var editedJurnalIdRegu = jurnalData.id_regu;
		
							// Tambahkan opsi untuk setiap survey
							data.forEach(survey => {
								if (survey.id === editedJurnalIdRegu) {
									selectRegu.append(`<option value="${survey.id}" selected>${survey.nama}</option>`);
								} else {
									selectRegu.append(`<option value="${survey.id}">${survey.nama}</option>`);
								}
							});
						},
						error: function(xhr, status, error) {
							console.error('Error:', error);
						}
					});
				}
			},
			error: function(error) {
				console.error('Error fetching survey data:', error);
				selectRegu.append('<option value="">Error fetching data</option>');
			}
		});
		
    });


});
