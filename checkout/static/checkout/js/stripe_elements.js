let publicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(publicKey);
let elements = stripe.elements();
let style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
let card = elements.create('card', { style: style });
card.mount('#card-element');

// Stripe validation

function errorMessageHTML(message) {
    return `
    <span class="icon" role="alert">
        <i class="fas fa-times"></i>
    </span>
    <span>${message}</span>
    `;
}


card.addEventListener('change', function (e) {
    let errorDiv = $('#card-errors');

    if (e.error) {
        $(errorDiv).html(errorMessageHTML(e.error.message));
    } else {
        errorDiv.textContent = '';
    }
});

// Handle stripe card form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    console.log(clientSecret)
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function (result) {
        if (result.error) {
            let errorDiv = document.getElementById('card-errors');
            $(errorDiv).html(errorMessageHTML(result.error.message));

            
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);

            card.update({ 'disabled': false });
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                console.log("succeeded")
                form.submit();
            }
        }
    });
});
