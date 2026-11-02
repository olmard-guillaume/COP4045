#Olmard Guillaume


# Problem 2: University Parking Permits



class ParkingPermit:
    """Store common information for a parking permit."""

    def __init__(
        self,
        car_owner_name: str,
        purchased_months: int,
        fee_schedule_dict: dict[str, float],
    ) -> None:
        """Initialize the car owner's name, months purchased, and fee schedule."""
        self.car_owner_name: str = car_owner_name
        self.purchased_months: int = purchased_months
        self.fee_schedule: dict[str, float] = fee_schedule_dict

    def cost(self) -> float:
        """Return the cost for a basic permit."""
        return 0.0

    def __str__(self) -> str:
        """Return a readable description of the permit."""
        return (
            f"Parking Permit Owner: {self.car_owner_name}, "
            f"Months Purchased: {self.purchased_months}, "
            f"Cost: ${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the permit."""
        return (
            f"ParkingPermit({self.car_owner_name!r}, "
            f"{self.purchased_months!r}, {self.fee_schedule!r})"
        )


class StudentPermit(ParkingPermit):
    """Represent a student parking permit."""

    def __init__(
        self,
        car_owner_name: str,
        purchased_months: int,
        fee_schedule_dict: dict[str, float],
        number_of_vehicles_registered: int,
    ) -> None:
        """Initialize a student permit and its registered vehicle count."""
        super().__init__(
            car_owner_name, purchased_months, fee_schedule_dict
        )
        self.number_of_vehicles_registered: int = (
            number_of_vehicles_registered
        )

    def cost(self) -> float:
        """Calculate student fees and one-time fees for extra vehicles."""
        monthly_fee: float = self.fee_schedule["student_monthly"]
        extra_vehicle_fee: float = self.fee_schedule["extra_vehicle"]

        extra_vehicles: int = max(
            0, self.number_of_vehicles_registered - 1
        )

        return (
            monthly_fee * self.purchased_months
            + extra_vehicle_fee * extra_vehicles
        )

    def __str__(self) -> str:
        """Return a readable description of the student permit."""
        return (
            f"Student Permit Owner: {self.car_owner_name}, "
            f"Months Purchased: {self.purchased_months}, "
            f"Vehicles Registered: "
            f"{self.number_of_vehicles_registered}, "
            f"Cost: ${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the student permit."""
        return (
            f"StudentPermit({self.car_owner_name!r}, "
            f"{self.purchased_months!r}, {self.fee_schedule!r}, "
            f"{self.number_of_vehicles_registered!r})"
        )


class FacultyPermit(ParkingPermit):
    """Represent a faculty permit with optional garage access."""

    def __init__(
        self,
        car_owner_name: str,
        purchased_months: int,
        fee_schedule_dict: dict[str, float],
        garage_access: bool,
    ) -> None:
        """Initialize a faculty permit and its garage-access status."""
        super().__init__(
            car_owner_name, purchased_months, fee_schedule_dict
        )
        self.garage_access: bool = garage_access

    def cost(self) -> float:
        """Calculate faculty fees, including garage access if selected."""
        monthly_fee: float = self.fee_schedule["faculty_monthly"]
        garage_monthly_fee: float = self.fee_schedule["garage_monthly"]

        total_cost: float = monthly_fee * self.purchased_months

        if self.garage_access:
            total_cost += garage_monthly_fee * self.purchased_months

        return total_cost

    def __str__(self) -> str:
        """Return a readable description of the faculty permit."""
        return (
            f"Faculty Permit Owner: {self.car_owner_name}, "
            f"Months Purchased: {self.purchased_months}, "
            f"Garage Access: {self.garage_access}, "
            f"Cost: ${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the faculty permit."""
        return (
            f"FacultyPermit({self.car_owner_name!r}, "
            f"{self.purchased_months!r}, {self.fee_schedule!r}, "
            f"{self.garage_access!r})"
        )


def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each car owner's permit cost and return total revenue."""
    total_revenue: float = 0.0

    for permit in permits:
        print(f"{permit.car_owner_name}: ${permit.cost():.2f}")
        total_revenue += permit.cost()

    return total_revenue


def main() -> None:
    """Create sample permits and display the objects and total revenue."""
    fee_schedule: dict[str, float] = {
        "student_monthly": 25.0,
        "extra_vehicle": 10.0,
        "faculty_monthly": 40.0,
        "garage_monthly": 15.0,
    }

    student_one: StudentPermit = StudentPermit(
        "Alex Johnson", 12, fee_schedule, 2
    )
    student_two: StudentPermit = StudentPermit(
        "Taylor Smith", 6, fee_schedule, 1
    )
    faculty_one: FacultyPermit = FacultyPermit(
        "Jordan Lee", 12, fee_schedule, True
    )
    faculty_two: FacultyPermit = FacultyPermit(
        "Morgan Davis", 6, fee_schedule, False
    )

    permits: list[ParkingPermit] = [
        student_one,
        student_two,
        faculty_one,
        faculty_two,
    ]

    print("Parking Permit Objects")
    print("----------------------")

    for permit in permits:
        print(permit)
        print(repr(permit))

    print("\nPermit Cost Summary")
    print("-------------------")

    total_revenue: float = summarize_list(permits)
    print(f"Total Revenue: ${total_revenue:.2f}")


if __name__ == "__main__":
    main()