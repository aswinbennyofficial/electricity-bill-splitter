import math

def calculate_proportion_based(total_units, bottom_floor_units, total_bill):
    top_floor_units = total_units - bottom_floor_units
    bottom_floor_percentage = bottom_floor_units / total_units
    top_floor_percentage = top_floor_units / total_units
    
    bottom_floor_bill = total_bill * bottom_floor_percentage
    top_floor_bill = total_bill * top_floor_percentage
    
    return {
        "Bottom Floor": round(bottom_floor_bill, 2),
        "Top Floor": round(top_floor_bill, 2)
    }

def calculate_slab_based(bottom_floor_units, top_floor_units, slab_utilization, slab_rates, total_bill):
    total_units = bottom_floor_units + top_floor_units
    
    # Initialize variables for each floor's usage in each slab
    bottom_floor_slab = [0, 0, 0]
    top_floor_slab = [0, 0, 0]
    
    # Allocate units for slab 1
    slab_1_quota = slab_utilization[0] / 2
    bottom_floor_slab[0] = min(bottom_floor_units, slab_1_quota)
    top_floor_slab[0] = min(top_floor_units, slab_1_quota)
    
    bottom_floor_remaining = max(0, bottom_floor_units - bottom_floor_slab[0])
    top_floor_remaining = max(0, top_floor_units - top_floor_slab[0])
    
    # Allocate units for slab 2
    slab_2_quota = slab_utilization[1] / 2
    bottom_floor_slab[1] = min(bottom_floor_remaining, slab_2_quota)
    top_floor_slab[1] = min(top_floor_remaining, slab_2_quota)
    
    bottom_floor_remaining = max(0, bottom_floor_remaining - bottom_floor_slab[1])
    top_floor_remaining = max(0, top_floor_remaining - top_floor_slab[1])
    
    # Allocate remaining units to the available quota in slab 1 and 2
    unused_slab_1 = slab_utilization[0] - (bottom_floor_slab[0] + top_floor_slab[0])
    unused_slab_2 = slab_utilization[1] - (bottom_floor_slab[1] + top_floor_slab[1])
    
    # Allocate bottom floor remaining units
    if bottom_floor_remaining > 0:
        additional_slab_1 = min(bottom_floor_remaining, unused_slab_1)
        bottom_floor_slab[0] += additional_slab_1
        bottom_floor_remaining -= additional_slab_1
        unused_slab_1 -= additional_slab_1
        
        additional_slab_2 = min(bottom_floor_remaining, unused_slab_2)
        bottom_floor_slab[1] += additional_slab_2
        bottom_floor_remaining -= additional_slab_2
        unused_slab_2 -= additional_slab_2
    
    # Allocate top floor remaining units
    if top_floor_remaining > 0:
        additional_slab_1 = min(top_floor_remaining, unused_slab_1)
        top_floor_slab[0] += additional_slab_1
        top_floor_remaining -= additional_slab_1
        
        additional_slab_2 = min(top_floor_remaining, unused_slab_2)
        top_floor_slab[1] += additional_slab_2
        top_floor_remaining -= additional_slab_2
    
    # Allocate any remaining units to slab 3 (top floor only)
    top_floor_slab[2] = top_floor_remaining
    
    # Calculate costs
    bottom_floor_cost = sum(usage * rate for usage, rate in zip(bottom_floor_slab, slab_rates))
    top_floor_cost = sum(usage * rate for usage, rate in zip(top_floor_slab, slab_rates))
    
    # Calculate and apply subsidy
    total_cost = bottom_floor_cost + top_floor_cost
    subsidy = total_cost - total_bill
    subsidy_per_floor = subsidy / 2
    
    bottom_floor_bill = bottom_floor_cost - subsidy_per_floor
    top_floor_bill = top_floor_cost - subsidy_per_floor
    
    return {
        "Bottom Floor": round(bottom_floor_bill, 2),
        "Top Floor": round(top_floor_bill, 2),
        "Bottom Floor Slab Usage": bottom_floor_slab,
        "Top Floor Slab Usage": top_floor_slab,
        "Total Cost": total_cost,
        "Subsidy": subsidy
    }

def calculate_total_metrics(bottom_floor_units, top_floor_units, slab_utilization, slab_rates, total_bill, slab_result):
    total_units = bottom_floor_units + top_floor_units
    total_slab_usage = [sum(x) for x in zip(slab_result["Bottom Floor Slab Usage"], slab_result["Top Floor Slab Usage"])]
    total_cost_before_subsidy = slab_result["Total Cost"]
    subsidy = slab_result["Subsidy"]
    net_payable = total_bill

    return {
        "Total Usage": total_units,
        "Slab-wise Total Usage": total_slab_usage,
        "Total Cost Before Subsidy": round(total_cost_before_subsidy, 2),
        "Discount (Subsidy)": round(subsidy, 2),
        "Net Payable": round(net_payable, 2)
    }

def main():
    bottom_floor_units = 262
    top_floor_units = 614
    total_bill = 5055
    slab_utilization = [217, 433, 226]  # Units utilized in each slab
    slab_rates = [4.54, 6.76, 7.75]
    
    proportion_result = calculate_proportion_based(bottom_floor_units + top_floor_units, bottom_floor_units, total_bill)
    slab_result = calculate_slab_based(bottom_floor_units, top_floor_units, slab_utilization, slab_rates, total_bill)
    total_metrics = calculate_total_metrics(bottom_floor_units, top_floor_units, slab_utilization, slab_rates, total_bill, slab_result)
    
    print("Proportion-based calculation:")
    for floor, amount in proportion_result.items():
        print(f"{floor}: {amount} Rs")
    
    print("\nSlab-based calculation:")
    for floor, amount in slab_result.items():
        if "Usage" not in floor and floor not in ["Total Cost", "Subsidy"]:
            print(f"{floor}: {amount} Rs")
        elif "Usage" in floor:
            print(f"{floor}: {amount}")
    
    print("\nTotal Metrics:")
    for metric, value in total_metrics.items():
        if metric == "Slab-wise Total Usage":
            print(f"{metric}:")
            for i, usage in enumerate(value):
                print(f"  Slab {i+1}: {usage} units")
        else:
            print(f"{metric}: {value}")

if __name__ == "__main__":
    main()
