// Ajax untuk mengambil data jurnal untuk diedit
$(document).on('click', '.edit-jurnal', function(e) {
	e.preventDefault();
	var jurnalId = $(this).data('id');
	$.ajax({
		type: 'GET',
		url: '/edit_jurnal/' + jurnalId + '/',
		success: function(data) {
			$('#edit_tanggal').val(data.tanggal);
			$('#edit_skp_tahunan').val(data.skp_tahunan);
			$('#edit_id_regu').val(data.id_regu);
			$('#edit_jurnal_harian').val(data.jurnal_harian);
			$('#edit_jumlah').val(data.jumlah);
			$('#edit_satuan').val(data.satuan);
			$('#edit_jam_mulai').val(data.jam_mulai);
			$('#edit_jam_selesai').val(data.jam_selesai);
			$('#edit_nilai').val(data.nilai);
			$('#edit_komentar').val(data.komentar);
			$('#edit_tanggal_isi').val(data.tanggal_isi);
			$('#editJurnalForm').attr('action', '/update_jurnal/' + jurnalId + '/');
			$('#editJurnalModal').modal('show');
		},
		error: function(xhr, status, error) {
			console.error('Error:', error);
			// Tampilkan pesan kesalahan kepada pengguna
			$('#errorMessage').text('Gagal memuat data jurnal. Silakan coba lagi.');
			$('#errorMessage').show();
		}
	});
});


// Ajax untuk mengirim data pembaruan jurnal
$(document).ready(function() {
	$('#editJurnalForm').submit(function(e) {
		e.preventDefault();
		var form = $(this);
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			success: function(response) {
				// Tutup modal setelah berhasil
				$('#editJurnalModal').modal('hide');
				// Tampilkan notifikasi sukses
				Swal.fire({
					icon: 'success',
					title: 'Berhasil!',
					text: 'Jurnal berhasil diperbarui.'
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
	$(document).on('click', '.delete-jurnal', function(e) {
		e.preventDefault();
		var jurnalId = $(this).data('id');
		Swal.fire({
			title: 'Kamu yakin?',
			text: "Jurnal akan dihapus secara permanen!",
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
					url: '/delete_jurnal/' + jurnalId + '/',
					data: {
						csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
					},
					success: function(response) {
						Swal.fire({
							icon: 'success',
							title: 'Berhasil!',
							text: 'Jurnal berhasil dihapus.'
						}).then((result) => {
							location.reload();
						});
					},
					error: function(xhr, status, error) {
						console.error('Error:', error);
						Swal.fire({
							icon: 'error',
							title: 'Gagal!',
							text: 'Terjadi kesalahan saat menghapus data jurnal.'
						});
					}
				});
			}
		});
	});
});


});