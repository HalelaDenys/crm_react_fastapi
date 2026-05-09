from dtos.dto import MapperDTO


def map_category_to_buttons(categories: list[dict]):
    return [
        MapperDTO(
            text=category["name"],
            call=f"category:{category['id']}:1",
        )
        for category in categories
    ]


def map_service_to_buttons(
    services: dict[list[dict], bool],
) -> tuple[list[MapperDTO], bool]:
    services_list = services["service_data"]
    hes_next = services["hes_next"]

    if not services:
        return [], True

    return [
        MapperDTO(text=service["name"], call=f"service:{service['id']}")
        for service in services_list
    ], hes_next


def map_available_slots_to_buttons(available_slots: list[dict]):
    return [MapperDTO(text=slot["text"], call=slot["call"]) for slot in available_slots]
