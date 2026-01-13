# Logging Configuration Summary

## ✅ Configuration Complete

### 1. **settings.py LOGGING Configuration**

Enhanced logging configuration with project-specific loggers:

- **Console Handler** - Rich formatted output (DEBUG level, development only)
- **File Handlers**:
  - `django.log` - Django framework logs
  - `project.log` - Application general logs (10MB rotating)
  - `email.log` - Email/utils logs (5MB rotating)
  - `signals.log` - Signal logs (5MB rotating)

### 2. **Logger Setup**

Configured loggers for:

- `project` - General application logs (DEBUG in dev, INFO in production)
- `project.utils` - Email and utility function logs
- `project.signals` - Signal handler logs
- `project.views` - View function logs
- `django` - Django framework logs

### 3. **Usage Pattern**

In any Python file in the project, use:

```python
import logging

logger = logging.getLogger(__name__)

# Then use:
logger.debug("Detailed debug information")
logger.info("General informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.exception("Error with traceback")  # Use in except blocks
```

### 4. **Log Locations**

All logs are stored in `logs/` directory:

- `/logs/django.log` - Django framework logs
- `/logs/project.log` - Application logs
- `/logs/email.log` - Email sending logs
- `/logs/signals.log` - Signal processing logs

### 5. **Log Files Created**

✅ `logs/` directory created

### 6. **Files Updated**

1. **main/settings.py**

   - Enhanced LOGGING configuration
   - Added project-specific loggers
   - Added rotating file handlers for each module

2. **project/signals.py**

   - Added `import logging` and `logger = logging.getLogger(__name__)`
   - Replaced all `print()` statements with logger calls
   - Added detailed info/error logging
   - Uses `logger.exception()` for error details with traceback

3. **project/utils.py**
   - Changed logger from `"django"` to `logging.getLogger(__name__)`
   - Added debug logging for email preparation steps
   - Added info logging for email sending
   - Added exception logging with traceback
   - Tracks order ID, customer email, and amounts

### 7. **Log Examples**

#### Order Confirmation Flow:

```
2026-01-12 14:30:45 INFO project.signals Order created: #42 by John Doe
2026-01-12 14:30:45 DEBUG project.utils Preparing order confirmation email for Order #42
2026-01-12 14:30:45 DEBUG project.utils Rendering email templates for Order #42
2026-01-12 14:30:45 DEBUG project.utils Creating email message for john@example.com
2026-01-12 14:30:46 INFO project.utils Sending order confirmation email for Order #42 to john@example.com
2026-01-12 14:30:47 INFO project.utils Order confirmation email sent successfully for Order #42
```

#### Donation Processing:

```
2026-01-12 14:30:47 INFO project.signals Processing donation of $25.00 for Order #42
2026-01-12 14:30:47 DEBUG project.utils Preparing donation thank you email for Order #42 (Amount: $25.00)
2026-01-12 14:30:48 INFO project.utils Sending donation thank you email for Order #42 ($25.00) to john@example.com
2026-01-12 14:30:49 INFO project.signals Donation thank you email sent successfully for Order #42 (Amount: $25.00)
```

### 8. **Log Levels Explained**

| Level    | Usage                            | Example                                 |
| -------- | -------------------------------- | --------------------------------------- |
| DEBUG    | Detailed info for debugging      | Template rendering, context preparation |
| INFO     | General informational messages   | Order created, email sent successfully  |
| WARNING  | Warning messages (default level) | Missing data, unusual conditions        |
| ERROR    | Error messages                   | Failed email, database error            |
| CRITICAL | Critical errors                  | System failure                          |

### 9. **File Rotation**

Rotating file handlers automatically:

- Create backup files when limit reached (e.g., `project.log.1`, `project.log.2`)
- Preserve older logs for debugging
- Email logs: 5MB limit, keep 3 backups
- Project logs: 10MB limit, keep 5 backups

### 10. **Development vs Production**

**Development (DEBUG=True)**:

- Console output enabled with rich formatting
- DEBUG level logging for detailed info
- Colors and tracebacks in console

**Production (DEBUG=False)**:

- Console output disabled
- INFO level logging
- All logs written to rotating file handlers
- No debug information in console

### 11. **Testing Logs**

To test the logging system:

```python
# In Django shell: python manage.py shell
from project.models import Order, Customer
from project.utils import send_order_confirmation_email
import logging

# Enable debug logging
logging.getLogger("project").setLevel(logging.DEBUG)

# Get an order and trigger email
order = Order.objects.first()
send_order_confirmation_email(order)

# Check logs
# tail -f logs/email.log
```

Or via terminal:

```bash
# Watch email logs in real-time
tail -f logs/email.log

# View signal logs
tail -f logs/signals.log

# View project logs
tail -f logs/project.log
```

### 12. **Error Tracking**

All exceptions are logged with full traceback:

```python
try:
    # your code here
    pass
except Exception as e:
    logger.exception("Error context: %s", e)  # Includes traceback
```

Check logs for complete error information:

```bash
grep -i "error\|exception" logs/email.log
```

## ✅ Ready to Use

The logging system is now fully configured and integrated with:

- Order creation signals
- Email sending functions
- Error handling and exception reporting

All logs will be written to the `logs/` directory with appropriate rotation and formatting.
