// Ajax untuk mengambil data survey untuk diedit
$(document).on('click', '.edit-survey', function(e) {
	e.preventDefault();
	var surveyId = $(this).data('id');
	$.ajax({
		type: 'GET',
		url: '/edit_survey/' + surveyId + '/',
		success: function(data) {
			$('#edit_nama').val(data.nama);
			$('#edit_point_regu').val(data.point_regu);
			$('#editSurveyForm').attr('action', '/update_survey/' + surveyId + '/');
			$('#editSurveyModal').modal('show');
		},
		error: function(xhr, status, error) {
			console.error('Error:', error);
			// Tampilkan pesan kesalahan kepada pengguna
			$('#errorMessage').text('Gagal memuat data survey. Silakan coba lagi.');
			$('#errorMessage').show();
		}
	});
});


// Ajax untuk mengirim data pembaruan survey
$(document).ready(function() {
	$('#editSurveyForm').submit(function(e) {
		e.preventDefault();
		var form = $(this);
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			success: function(response) {
				// Tutup modal setelah berhasil
				$('#editSurveyModal').modal('hide');
				// Tampilkan notifikasi sukses
				Swal.fire({
					icon: 'success',
					title: 'Berhasil!',
					text: 'Survey berhasil diperbarui.'
				}).then((result) => {
					// Lakukan reloading jika diperlukan
					location.reload(); // Reload halaman
				});
			},
			error: function(response) {
				// Tangani kesalahan validasi jika ada
				var errors = JSON.parse(response.responseText).errors;
				console.log(errors); // Lakukan sesuai kebutuhan, misalnya, tampilkan pesan kesalahan
			}
		});
	});


// Ajax untuk mengirim hapus data
$(document).ready(function() {
	$(document).on('click', '.delete-survey', function(e) {
		e.preventDefault();
		var surveyId = $(this).data('id');
		Swal.fire({
			title: 'Kamu yakin?',
			text: "Survey akan dihapus secara permanen!",
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#d33',
			cancelButtonColor: '#3085d6',
			confirmButtonText: 'Hapus',
			cancelButtonText: 'Batal'
		}).then((result) => {
			if (result.isConfirmed) {
				$.ajax({
					type: 'POST',
					url: '/delete_survey/' + surveyId + '/',
					data: {
						csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
					},
					success: function(response) {
						Swal.fire({
							icon: 'success',
							title: 'Berhasil!',
							text: 'Survey berhasil dihapus.'
						}).then((result) => {
							location.reload();
						});
					},
					error: function(xhr, status, error) {
						console.error('Error:', error);
						Swal.fire({
							icon: 'error',
							title: 'Gagal!',
							text: 'Terjadi kesalahan saat menghapus data survey.'
						});
					}
				});
			}
		});
	});
});


});