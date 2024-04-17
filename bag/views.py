from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """View the shopping bag"""

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of a product to bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()}'
                                 + f'{product.name} quantity to '
                                 + f'{bag[item_id]['items_by_size'][size]}.')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()}'
                                 + f'{product.name} to bag.')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()}'
                             + f'{product.name} to bag.')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated quantity of {product.name} to '
                             + f'{product.quantity}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to bag.')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust items within bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()}'
                             + f'{product.name} quantity to '
                             + f'{bag[item_id]['items_by_size'][size]}.')
        else:
            del bag[item_id]['items_by_size'][size]
            del_sizes_of_items_if_empty(bag, item_id)
            messages.success(request, f'Removed size {size.upper()}'
                             + f'{product.name} from bag.')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to '
                             + f'{bag[item_id]}.')
        else:
            del bag[item_id]
            messages.success(request, f'Removed {product.name} from bag.')

    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            del_sizes_of_items_if_empty(bag, item_id)
            messages.success(request, f'Removed size {size.upper()}'
                             + f'{product.name} from bag.')
        else:
            del bag[item_id]
            messages.success(request, f'Removed {product.name} from bag.')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


def del_sizes_of_items_if_empty(bag, item_id):
    if not bag[item_id]['items_by_size']:
        bag.pop(item_id)
