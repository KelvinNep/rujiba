// Ajax untuk mengambil data rekapulasi untuk diedit
$(document).on('click', '.edit-rekap', function(e) {
	e.preventDefault();
	var rekapId = $(this).data('id');
	$.ajax({
		url: '/edit_rekap/' + rekapId + '/',
		type: 'GET',
		dataType: 'json',
		success: function(data) {
			// Isi form dengan data yang didapatkan
			$('#edit_nip').val(data.nip);
			$('#edit_nama').val(data.nama);
			$('#edit_unit_kerja').val(data.unit_kerja);
			$('#edit_terlambat').val(data.terlambat);
			$('#edit_pulang_cepat').val(data.pulang_cepat);
			$('#edit_terlambat_menit').val(data.terlambat_menit);
			$('#edit_pulang_cepat_menit').val(data.pulang_cepat_menit);
			$('#edit_tanpa_keterangan').val(data.tanpa_keterangan);
			$('#edit_terlambat_izin').val(data.terlambat_izin);
			$('#edit_pulang_cepat_izin').val(data.pulang_cepat_izin);
			$('#edit_lupa_absen_masuk').val(data.lupa_absen_masuk);
			$('#edit_lupa_absen_pulang').val(data.lupa_absen_pulang);
			$('#edit_full').val(data.full);
			$('#edit_half').val(data.half);
			$('#edit_total').val(data.total);

			// Set the action URL of the form
			$('#editRekapForm').attr('action', '/update_rekap/' + rekapId + '/');

			// Tampilkan modal
			$('#editRekapModal').modal('show');
		},
		error: function(xhr, status, error) {
			console.error('Error:', error);
			$('#errorMessage').text('Gagal memuat data rekapitulasi. Silakan coba lagi.');
			$('#errorMessage').show();
		}
	});
});


// Ajax untuk mengirim data pembaruan rekapulasi
$(document).ready(function() {
	$('#editRekapForm').submit(function(e) {
		e.preventDefault();
		var form = $(this);
		console.log(form.serialize())
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			success: function(response) {
				// Tutup modal setelah berhasil
				$('#editRekapForm').modal('hide');
				// Tampilkan notifikasi sukses
				Swal.fire({
					icon: 'success',
					title: 'Berhasil!',
					text: 'Rekapulasi berhasil diperbarui.'
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
	$(document).on('click', '.delete-rekap', function(e) {
		e.preventDefault();
		var rekapId = $(this).data('id');
		Swal.fire({
			title: 'Kamu yakin?',
			text: "Rekapulasi akan dihapus secara permanen!",
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
					url: '/delete_rekap/' + rekapId + '/',
					data: {
						csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
					},
					success: function(response) {
						Swal.fire({
							icon: 'success',
							title: 'Berhasil!',
							text: 'Rekapulasi berhasil dihapus.'
						}).then((result) => {
							location.reload();
						});
					},
					error: function(xhr, status, error) {
						console.error('Error:', error);
						Swal.fire({
							icon: 'error',
							title: 'Gagal!',
							text: 'Terjadi kesalahan saat menghapus data rekapulasi.'
						});
					}
				});
			}
		});
	});
});


});