$(document).ready(function() {
    // Mendapatkan token CSRF dari meta tag
    console.log('ppp')
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    
    // Menangani klik tombol dengan class .btngenerate
    $(document).on('click', '.btngenerate', function(e) {
        e.preventDefault();
        
        // Mengambil nilai periode dan tahun dari dropdown
        var period = $('#periodDropdown').val();
        var year = $('#yearDropdown').val();
        console.log("Period:", period, "Year:", year);
  
        // Melakukan permintaan AJAX ke endpoint /process-data/
        $.ajax({
            type: 'POST',
            url: '/process-data/',
            data: {
                period: period,
                year: year
            },
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken  
            },
            success: function(response) {
                console.log("AJAX request successful");
                // Menangani respons sukses
                if (response.no_data) {
                    Swal.fire({
                        icon: 'question',
                        title: 'Konfirmasi',
                        text: 'Tidak ada data yang tersedia. Apakah Anda ingin membuat data baru?',
                        showCancelButton: true,
                        confirmButtonText: 'Ya',
                        cancelButtonText: 'Tidak',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            // Jika dikonfirmasi, lakukan permintaan lain untuk membuat data baru
                            $.ajax({
                                type: 'POST',
                                url: '/process-data/',
                                data: {
                                    period: period,
                                    year: year,
                                    generate_new: true // Menandakan untuk membuat data baru
                                },
                                dataType: 'json',
                                headers: {
                                    'X-CSRFToken': csrfToken  // Menyertakan token CSRF dalam header
                                },
                                success: function(response) {
                                    Swal.fire({
                                        icon: 'success',  
                                        title: 'Generate Periode',
                                        text: 'Data telah berhasil dihasilkan!',
                                    });
                                    // Perbarui dashboard dengan data baru
                                    updateDashboard(response.new_data);
                                },
                                error: function(xhr, status, error) {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Gagal menghasilkan data. Silakan coba lagi nanti.',
                                    });
                                }
                            });
                        }
                    });
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Generate Periode',
                        text: 'Data telah berhasil dihasilkan!',
                    });
                    // Perbarui dashboard dengan data baru
                    updateDashboard(response.new_data);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX request failed:", error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Gagal menghasilkan data. Silakan coba lagi nanti.',
                });
            }
        });
    });
  
    // Fungsi untuk memperbarui dashboard
    function updateDashboard(data) {
        console.log("Updating dashboard with data:", data);
        var tableBody = $('#rankingTable');
        tableBody.empty(); 
        data.forEach(function(row) {
            var tr = $('<tr></tr>');
            tr.append('<td>' + row.regu + '</td>');
            tr.append('<td>' + row.nilai_absen + '</td>');
            tr.append('<td>' + row.nilai_jurnal + '</td>');
            tr.append('<td>' + row.nilai_kuisioner + '</td>');
            tr.append('<td>' + row.status + '</td>');
            tableBody.append(tr);
        });
    }
});
