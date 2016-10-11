from ..tools import wellname_to_index
import pandas as pd

def picklist_to_tecan_evo_picklist_file(picklist, filename,
                                        change_tips_between_dispenses=True,
                                        tecan_plate_names=None):

    tecan_plate_names = {} if tecan_plate_names is None else tecan_plate_names
    def plate_to_tecan_name(plate):
        return tecan_plate_names.get(plate, plate.name)

    columns = [
        "Action", "RackLabel", "RackID", "RackType",
        "Position", "TubeID", "Volume", "LiquidClass",
        "TipType", "TipMask"
    ]

    rows = []
    for transfer in picklist.transfers_list:
        volume = "%.01f" % (transfer.volume / 1e-6)
        absorb = {
            "Action": "A",
            "RackLabel": plate_to_tecan_name(transfer.source_well.plate),
            "Position": wellname_to_index(
                transfer.source_well.name,
                transfer.source_well.plate.num_wells,
                direction="column"
            ),
            "Volume": volume
        }
        dispense = {
            "Action": "D",
            "RackLabel": plate_to_tecan_name(transfer.destination_well.plate),
            "Position": wellname_to_index(
                transfer.destination_well.name,
                transfer.destination_well.plate.num_wells,
                direction="column"
            ),
            "Volume":  volume
        }
        row = [absorb, dispense]
        if change_tips_between_dispenses:
            row += [{"Action": "W"}]
        rows += row

    df = pd.DataFrame.from_records(rows, columns=columns)
    df.to_csv(filename, sep=";", header=False, index=False)
