ITEM_PRICE = 1.00
DISCOUNT_THRESHOLD = 10
DISCOUNT_RATE = 0.05
SALES_TAX_RATE = 0.075


def main():
    try:
        items = int(input("Enter the number of items purchased: "))
    except ValueError:
        print("Please enter a whole number.")
        return

    if items < 0:
        print("Number of items cannot be negative.")
        return

    subtotal = items * ITEM_PRICE

    if items >= DISCOUNT_THRESHOLD:
        subtotal *= (1 - DISCOUNT_RATE)

    total_after_tax = subtotal * (1 + SALES_TAX_RATE)
    tax_amount = total_after_tax - subtotal

    print(f"Total before tax: ${subtotal:.2f}")
    print(f"Tax amount:       ${tax_amount:.2f}")
    print(f"Total after tax:  ${total_after_tax:.2f}")


if __name__ == "__main__":
    main()
