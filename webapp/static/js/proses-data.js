$(document).ready(function() {
    $('.proses-data').click(function() {
        var period = $('#periodDropdown').val();
        var year = $('#yearDropdown').val();
        
        // Show loading indicator only if there's data available
        $.ajax({
            type: 'GET',  // Use GET request to check data availability
            url: '/proses-data/',
            data: {
                'period': period,
                'year': year,
            },
            success: function(response) {
                if (response.has_data) {
                    // Data available, show loading indicator
                    Swal.fire({
                        title: 'Loading...',
                        allowOutsideClick: false,
                        showConfirmButton: false,
                        willOpen: () => {
                            Swal.showLoading();
                        }
                    });

                    // Proceed with POST request to process data
                    $.ajax({
                        type: 'POST',
                        url: '/proses-data/',
                        data: {
                            'period': period,
                            'year': year,
                            'csrfmiddlewaretoken': $('meta[name=csrf-token]').attr('content')
                        },
                        success: function(response) {
                            // Close loading indicator
                            Swal.close();

                            // Handle success, e.g., show success message or update UI
                            Swal.fire({
                                icon: 'success',
                                title: 'Success',
                                text: 'Data successfully processed and predictions saved.'
                            });

                            // Reload or update the UI as needed
                            location.reload();  // Example: Reload the page after processing
                        },
                        error: function(error) {
                            // Close loading indicator
                            Swal.close();

                            // Handle error, e.g., show error message
                            Swal.fire({
                                icon: 'error',
                                title: 'Error',
                                text: 'Failed to process data.'
                            });
                        }
                    });
                } else {
                    // No data available, show error message
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Tidak ada data yang ditemukan.'
                    });
                }
            },
            error: function(error) {
                // Handle error in checking data availability
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to check data availability.'
                });
            }
        });
    });
});
