import base64
import logging
from io import BytesIO
from pathlib import Path

import qrcode
from django.http import HttpRequest
from exif import Image
from PIL import Image as PILImage

from project.models import PlantImage, PlantProfile

logger = logging.getLogger(__name__)

MONTHS = {
    0: "",
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def all_plants(request):
    return PlantProfile.objects.all()


def single_plant(pk, request: HttpRequest):
    if request.user.is_authenticated:
        plant = PlantProfile.all_objects.get(pk=pk)
    else:
        try:
            plant = PlantProfile.objects.get(pk=pk)
        except PlantProfile.DoesNotExist:
            plant = None

    # plant.bloom_start = MONTHS.get(plant.bloom_start, "")
    # plant.bloom_end = MONTHS.get(plant.bloom_end, "")

    # plant.harvesting_start = MONTHS[plant.harvesting_start]
    return plant


def plant_primary_image(plant: PlantProfile):
    plant_image = PlantImage.objects.filter(
        plant_profile=plant, morphology_aspect=7
    ).first()
    return plant_image


def resize_image(image_path: str, max_width: int, max_height: int):
    with PILImage.open(image_path) as img:
        img.thumbnail((max_width, max_height))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        return buffered


def plant_light_range(plant: PlantProfile):
    if plant.full_sun and plant.full_shade:
        return "Full Sun to Full Shade"
    elif plant.full_sun and plant.part_shade:
        return "Full Sun to Part Shade"
    elif plant.part_shade and plant.full_shade:
        return "Part Shade to Full Shade"
    elif plant.full_sun:
        return "Full Sun"
    elif plant.part_shade:
        return "Part Shade"
    elif plant.full_shade:
        return "Full Shade"
    return "Unknown Light Range"


def plant_moisture_range(plant: PlantProfile):
    if plant.moisture_dry and plant.moisture_wet:
        return "Dry to Wet"
    elif plant.moisture_dry and plant.moisture_medium:
        return "Dry to Medium"
    elif plant.moisture_medium and plant.moisture_wet:
        return "Medium to Wet"
    elif plant.moisture_dry:
        return "Dry"
    elif plant.moisture_medium:
        return "Medium"
    elif plant.moisture_wet:
        return "Wet"
    return "Unknown Moisture Range"


def plant_split_long_string(input_string: str, max_length: int = 100) -> list[str]:
    """Splits a long string into a list of strings if the string contains 2 periods or more and input_string longer than 100 characters."""
    if input_string and len(input_string) > max_length and input_string.count(".") >= 2:
        return [
            sentence.strip() for sentence in input_string.split(".") if sentence.strip()
        ]
    return [input_string] if input_string else []


def plant_sowing_notes(plant: PlantProfile):
    if plant.sowing_notes:

        note_list = plant.sowing_notes.split(".")
        note_list = [note.strip() for note in note_list if note.strip()]
        return note_list
    return []


def plant_label_info(plant: PlantProfile, request: HttpRequest) -> list[str]:
    double_dormancy = None
    latin_name = plant.latin_name
    english_name = plant.english_name
    french_name = plant.french_name
    light_range = plant_light_range(plant)
    moisture_range = f"Moisture: {plant_moisture_range(plant)}"
    plant_size = f"{str(plant.max_height)}' tall, {str(plant.max_width)}' wide"
    bloom_period = f"Bloom: {MONTHS.get(plant.bloom_start, '')} - {MONTHS.get(plant.bloom_end, '')}"
    sowing_notes = plant_sowing_notes(plant)
    sowing_time = sow_before(plant)
    sowing_depth = plant.sowing_depth.sowing_depth

    if plant.double_dormancy:
        double_dormancy = "Double Dormancy"

    label_info = [
        latin_name,
        english_name,
        french_name,
        light_range,
        moisture_range,
        plant_size,
        bloom_period,
        *sowing_notes,  # Unpack the list items individually
    ]

    if sowing_time:
        label_info.append(sowing_time)

    if sowing_depth:
        label_info.append(sowing_depth)

    _stratification_need = stratification_need(plant)
    if _stratification_need:
        label_info.append(_stratification_need)

    if double_dormancy:
        label_info.append(double_dormancy)

    label_info.reverse()
    return label_info


def stratification_need(plant: PlantProfile):
    # consider plant.stratification_detail and plant.stratification_duration and return appropriate string
    stratification_detail = None
    stratification_duration = None

    if plant.double_dormancy:
        stratification_duration = "Stratify for 2 years"
        return stratification_duration

    if plant.stratification_detail:
        stratification_detail = plant.stratification_detail

    if plant.stratification_duration:
        stratification_duration = plant.stratification_duration.__str__()

    if stratification_detail and stratification_duration:
        return f"{stratification_detail} {stratification_duration}"

    elif stratification_detail:
        return stratification_detail

    elif stratification_duration:
        return f"Stratify for {stratification_duration}"

    return None


def sow_before(plant: PlantProfile):
    if not plant.stratification_duration:
        return "Sow anytime"
    duration = plant.stratification_duration.stratification_duration
    if not duration or duration == 0:
        return "Sow anytime"
    if duration == 30:
        return "Sow by March"
    elif duration == 60:
        return "Sow by February"
    elif duration == 90:
        return "Sow by January"
    elif duration == 120:
        return "Sow by December"
    elif duration == 180:
        return "Sow by November"
    else:
        return None


def is_plant_toxic(plant: PlantProfile):
    """Check if a plant is toxic based on its toxicity indicator."""
    not_toxic_options = ["Not known to be toxic", "Unknown", "None", ""]
    return str(plant.toxicity_indicator) not in not_toxic_options


def get_plants_without_images():
    # Returns a queryset of PlantProfile instances without associated PlantImage entries.
    return PlantProfile.all_objects.filter(images__isnull=True)


def is_valid_url(url: str) -> bool:
    """Check if a given string is a valid URL."""
    from django.core.exceptions import ValidationError
    from django.core.validators import URLValidator

    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


def get_image_gps_coordinates(image_path: Path) -> dict | None:
    try:
        with open(image_path, "rb") as img_f:
            img = Image(img_f)
            if img.has_exif:
                if hasattr(img, "gps_latitude") and hasattr(img, "gps_longitude"):

                    lat = img.gps_latitude
                    lon = img.gps_longitude
                    lat_ref = img.gps_latitude_ref
                    lon_ref = img.gps_longitude_ref

                    lat_decimal = (
                        lat[0] + lat[1] / 60 + lat[2] / 3600
                        if lat_ref == "N"
                        else -(lat[0] + lat[1] / 60 + lat[2] / 3600)
                    )
                    lon_decimal = (
                        lon[0] + lon[1] / 60 + lon[2] / 3600
                        if lon_ref == "E"
                        else -(lon[0] + lon[1] / 60 + lon[2] / 3600)
                    )

                    return {
                        "latitude": lat_decimal,
                        "longitude": lon_decimal,
                    }

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {image_path}")
    except Exception:
        raise Exception(f"Error processing file {image_path}")

    return None


def flush_gps_coordinates(image_path: Path) -> dict | None:

    gps_coordinates = get_image_gps_coordinates(image_path)
    if not gps_coordinates:
        return None

    try:
        with open(image_path, "rb") as img_f:
            img = Image(img_f)
            if hasattr(img, "gps_latitude"):
                del img.gps_latitude

            if hasattr(img, "gps_longitude"):
                del img.gps_longitude

            if hasattr(img, "gps_latitude_ref"):
                del img.gps_latitude_ref

            if hasattr(img, "gps_longitude_ref"):
                del img.gps_longitude_ref

        with open(image_path, "wb") as new_img_f:
            new_img_f.write(img.get_file())

    except Exception:
        raise Exception(f"Error processing file {image_path}")

    return gps_coordinates


def create_qr_code(data: str, box_size: int = 10, border: int = 4):
    # createn a QR code and return as a base64 string
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str


def create_qr_code_image(data: str, box_size: int = 10, border: int = 4):
    # create a QR code and return as a PIL Image
    # good for direct embedding in PDFs
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


# define a method that searches the html content on iNaturalist for a given plant name and searches the iNaturalist taxon ID of the plant.
# Exemple, when searching for "Quercus muehlenbergii" on inaturalist, a list of results is returned as a web page, and
# within the html content of the page, we can find the taxon id of the plant.
# the taxon id is embeded in the page results as https://www.inaturalist.org/taxa/54783-Quercus-muehlenbergii
def get_inaturalist_taxon_id(plant_name: str) -> int | None:
    import requests
    from bs4 import BeautifulSoup

    search_url = f"https://www.inaturalist.org/search?q={plant_name}&search_type=taxa"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # taxon_link is in the format <a href="/taxa/54783-Quercus-muehlenbergii">Quercus muehlenbergii</a>
        # Find the first link matches anchor tag with href containing /taxa/ followed by digits and a hyphen
        taxon_link = soup.find(
            "a",
            href=lambda href: href
            and "/taxa/" in href
            and any(char.isdigit() for char in href.split("/")[2].split("-")[0]),
        )

        if taxon_link:
            href = taxon_link["href"]
            taxon_id_str = href.split("/")[2].split("-")[0]
            try:
                taxon_id = int(taxon_id_str)
                return taxon_id
            except ValueError:
                return None
    return None


# ============================================================================
# SHOPPING CART & CHECKOUT UTILITIES
# ============================================================================


def get_or_create_customer_from_session(request):
    """
    Get the Customer object associated with the current session.
    If no customer_id in session, returns None.

    Args:
        request: Django request object

    Returns:
        Customer object or None
    """
    from project.models import Customer

    customer_id = request.session.get("customer_id")
    if not customer_id:
        return None

    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None


def set_customer_in_session(request, customer):
    """
    Store customer ID in the session.

    Args:
        request: Django request object
        customer: Customer object or customer ID
    """
    if isinstance(customer, int):
        request.session["customer_id"] = customer
    else:
        request.session["customer_id"] = customer.id
    request.session.modified = True


def add_to_cart(request, plant_profile, quantity=1):
    """
    Add a plant to the shopping cart or update quantity if already exists.

    Args:
        request: Django request object
        plant_profile: PlantProfile object or ID
        quantity: Quantity to add (default 1)

    Returns:
        ShoppingCart object or None if customer not in session
    """
    from project.models import PlantProfile as PlantProfileModel
    from project.models import ShoppingCart

    customer = get_or_create_customer_from_session(request)
    if not customer:
        return None

    if isinstance(plant_profile, int):
        plant_profile = PlantProfileModel.objects.get(id=plant_profile)

    cart_item, created = ShoppingCart.objects.get_or_create(
        customer=customer, plant_profile=plant_profile, defaults={"quantity": quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item


def update_cart_item(request, plant_profile, quantity):
    """
    Update the quantity of an item in the shopping cart.

    Args:
        request: Django request object
        plant_profile: PlantProfile object or ID
        quantity: New quantity (0 or negative removes the item)

    Returns:
        ShoppingCart object or None
    """
    from project.models import PlantProfile as PlantProfileModel
    from project.models import ShoppingCart

    customer = get_or_create_customer_from_session(request)
    if not customer:
        return None

    if isinstance(plant_profile, int):
        plant_profile = PlantProfileModel.objects.get(id=plant_profile)

    try:
        cart_item = ShoppingCart.objects.get(
            customer=customer, plant_profile=plant_profile
        )

        if quantity <= 0:
            cart_item.delete()
            return None

        cart_item.quantity = quantity
        cart_item.save()
        return cart_item
    except ShoppingCart.DoesNotExist:
        return None


def remove_from_cart(request, plant_profile):
    """
    Remove an item from the shopping cart.

    Args:
        request: Django request object
        plant_profile: PlantProfile object or ID

    Returns:
        Boolean indicating if item was removed
    """
    from project.models import PlantProfile as PlantProfileModel
    from project.models import ShoppingCart

    customer = get_or_create_customer_from_session(request)
    if not customer:
        return False

    if isinstance(plant_profile, int):
        plant_profile = PlantProfileModel.objects.get(id=plant_profile)

    try:
        cart_item = ShoppingCart.objects.get(
            customer=customer, plant_profile=plant_profile
        )
        cart_item.delete()
        return True
    except ShoppingCart.DoesNotExist:
        return False


def get_cart_items(request):
    """
    Get all items in the shopping cart for the current customer.

    Args:
        request: Django request object

    Returns:
        QuerySet of ShoppingCart items or empty QuerySet
    """
    from project.models import ShoppingCart

    customer = get_or_create_customer_from_session(request)
    if not customer:
        return ShoppingCart.objects.none()

    return ShoppingCart.objects.filter(customer=customer).select_related(
        "plant_profile"
    )


def get_cart_total(request):
    """
    Get the item count in the cart.
    Since seeds are free, this just returns the number of items.

    Args:
        request: Django request object

    Returns:
        Integer count of items in cart
    """
    cart_items = get_cart_items(request)
    return sum(item.quantity for item in cart_items)


def create_order_from_cart(request, donation_amount=0, notes=""):
    """
    Convert shopping cart items into an Order and OrderItems.
    Clears the cart after order creation.
    Seeds are free, but an optional donation can be included.

    Args:
        request: Django request object
        donation_amount: Optional donation amount (default 0)
        notes: Optional notes for the order

    Returns:
        Order object or None if cart is empty or customer not found
    """
    from decimal import Decimal

    from project.models import Order, OrderItem

    customer = get_or_create_customer_from_session(request)
    if not customer:
        return None

    cart_items = get_cart_items(request)
    if not cart_items.exists():
        return None

    # Ensure donation_amount is a Decimal
    if not isinstance(donation_amount, Decimal):
        donation_amount = Decimal(str(donation_amount))

    # Create the order
    order = Order.objects.create(
        customer=customer,
        donation_amount=donation_amount,
        notes=notes,
        status="pending",
    )

    # Create OrderItems from cart items (seeds are free)
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            plant_profile=cart_item.plant_profile,
            quantity=cart_item.quantity,
        )

    # Clear the shopping cart
    cart_items.delete()

    return order


def clear_cart(request):
    """
    Clear all items from the shopping cart.

    Args:
        request: Django request object

    Returns:
        Number of items deleted
    """
    cart_items = get_cart_items(request)
    count, _ = cart_items.delete()
    return count


def clear_session(request):
    """
    Clear customer ID from the session.

    Args:
        request: Django request object
    """
    if "customer_id" in request.session:
        del request.session["customer_id"]
    request.session.modified = True


# ============================================================================
# EMAIL UTILITIES
# ============================================================================


def send_order_confirmation_email(order):
    """
    Send order confirmation email to the customer.

    Args:
        order: Order object to send confirmation for

    Returns:
        Boolean indicating success
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.translation import gettext as _

    try:
        logger.debug("Preparing order confirmation email for Order #%s", order.id)

        # Prepare email context
        order_items = order.items.all().select_related("plant_profile")
        context = {
            "order": order,
            "order_items": order_items,
            "customer": order.customer,
        }

        # Render email templates
        subject = _("Order Confirmation - Order #%(order_id)d") % {"order_id": order.id}
        logger.debug("Rendering email templates for Order #%s", order.id)
        html_content = render_to_string(
            "project/emails/order_confirmation.html", context
        )
        text_content = render_to_string(
            "project/emails/order_confirmation.txt", context
        )

        # Create email
        logger.debug("Creating email message for %s", order.customer.email)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            to=[order.customer.email],
        )
        email.attach_alternative(html_content, "text/html")

        # Send email
        logger.info(
            "Sending order confirmation email for Order #%s to %s",
            order.id,
            order.customer.email,
        )
        email.send(fail_silently=False)
        logger.info(
            "Order confirmation email sent successfully for Order #%s", order.id
        )
        return True

    except Exception as e:
        logger.exception(
            "Error sending order confirmation email for Order #%s: %s",
            order.id,
            e,
        )
        return False


def send_donation_thank_you_email(order):
    """
    Send thank you email for a donation.

    Args:
        order: Order object with donation_amount > 0

    Returns:
        Boolean indicating success
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.translation import gettext as _

    if order.donation_amount <= 0:
        logger.debug(
            "Skipping donation email for Order #%s: donation_amount is %s",
            order.id,
            order.donation_amount,
        )
        return False

    try:
        logger.debug(
            "Preparing donation thank you email for Order #%s (Amount: $%s)",
            order.id,
            order.donation_amount,
        )

        # Prepare email context
        context = {
            "order": order,
            "customer": order.customer,
            "donation_amount": order.donation_amount,
        }

        # Render email templates
        subject = _("Thank You for Your Donation!")
        logger.debug("Rendering donation email templates for Order #%s", order.id)
        html_content = render_to_string(
            "project/emails/donation_thank_you.html", context
        )
        text_content = render_to_string(
            "project/emails/donation_thank_you.txt", context
        )

        # Create email
        logger.debug("Creating donation thank you email for %s", order.customer.email)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            to=[order.customer.email],
        )
        email.attach_alternative(html_content, "text/html")

        # Send email
        logger.info(
            "Sending donation thank you email for Order #%s ($%s) to %s",
            order.id,
            order.donation_amount,
            order.customer.email,
        )
        email.send(fail_silently=False)
        logger.info(
            "Donation thank you email sent successfully for Order #%s (Amount: $%s)",
            order.id,
            order.donation_amount,
        )
        return True

    except Exception as e:
        logger.exception(
            "Error sending donation thank you email for Order #%s: %s",
            order.id,
            e,
        )
        return False
