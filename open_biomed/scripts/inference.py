import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import argparse

from open_biomed.core.pipeline import InferencePipeline, EnsemblePipeline
from open_biomed.core.tool_misc import MutationToSequence
from open_biomed.data import Molecule, Text, Protein, Pocket
from open_biomed.tasks.aidd_tasks.protein_molecule_docking import VinaDockTask

os.environ["dataset_name"] = "BBBP"

def test_text_based_molecule_editing():
    pipeline = InferencePipeline(
        task="text_based_molecule_editing",
        model="molt5",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/logs/text_based_molecule_editing/molt5-fs_mol_edit/train/checkpoints/last.ckpt",
        device="cuda:0"
    )
    input_smiles = "Nc1[nH]c(C(=O)c2ccccc2)c(-c2ccccn2)c1C(=O)c1c[nH]c2ccc(Br)cc12"
    input_text = "This molecule can bind with recombinant human 15-LOX-1"
    outputs = pipeline.run(
        molecule=Molecule.from_smiles(input_smiles),
        text=Text.from_str(input_text),
    )
    print(f"Input SMILES: {input_smiles}")
    print(f"Input Text: {input_text}")
    print(outputs[0])
    return pipeline

def test_pocket_molecule_docking():
    pipeline = InferencePipeline(
        task="pocket_molecule_docking",
        model="pharmolix_fm",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/checkpoints/demo/pharmolix_fm.ckpt",
        device="cuda:0"
    )
    protein = Protein.from_pdb_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B.pdb")
    ligand = Molecule.from_sdf_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B_ref.sdf")
    pocket = Pocket.from_protein_ref_ligand(protein, ligand)
    outputs = pipeline.run(
        molecule=ligand,
        pocket=pocket,
    )
    print(outputs)
    return pipeline

def test_structure_based_drug_design():
    pipeline = InferencePipeline(
        task="structure_based_drug_design",
        model="pharmolix_fm",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/checkpoints/demo/pharmolix_fm.ckpt",
        device="cuda:0"
    )
    protein = Protein.from_pdb_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B.pdb")
    ligand = Molecule.from_sdf_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B_ref.sdf")
    pocket = Pocket.from_protein_ref_ligand(protein, ligand)
    outputs = pipeline.run(
        pocket=pocket
    )
    print(outputs)
    return pipeline

def test_protein_molecule_docking():
    try:
        protein = Protein.from_pdb_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B.pdb")
        ligand = Molecule.from_sdf_file("/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/tmp/sbdd/4xli_B_ref.sdf")
        vina = VinaDockTask(mode="dock")
        print(vina.run(ligand, protein)[0][0])
        return vina
    except:
        print("AutoDockVina not supported.")
    return vina
    
def test_molecule_question_answering():
    pipeline = InferencePipeline(
        task="molecule_question_answering",
        model="biot5",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/logs/molecule_question_answering/biot5-MQA/train/checkpoints/last.ckpt",
        device="cuda:0"
    )
    molecule = Molecule.from_smiles("C[C@@H]1CCCCO[C@@H](CN(C)C(=O)Cc2ccccc2)[C@@H](C)CN([C@@H](C)CO)C(=O)c2cc(NS(C)(=O)=O)ccc2O1")
    question = Text.from_str("Could you provide the systematic name of this compound according to IUPAC nomenclature?")
    outputs = pipeline.run(
        molecule=molecule,
        text=question,
    )
    print(outputs)
    return pipeline

def test_protein_question_answering():
    pipeline = InferencePipeline(
        task="protein_question_answering",
        model="biot5",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/logs/protein_question_answering/biot5-PQA/train/checkpoints/last.ckpt",
        device="cuda:0"
    )
    protein = Protein.from_fasta("MRVGVIRFPGSNCDRDVHHVLELAGAEPEYVWWNQRNLDHLDAVVIPGGFSYGDYLRAGAIAAITPVMDAVRELVREEKPVLGICNGAQILAEVGLVPGVFTVNEHPKFNCQWTELRVKTTRTPFTGLFKKDEVIRMPVAHAEGRYYHDNISEVWENDQVVLQFHGENPNGSLDGITGVCDESGLVCAVMPHPERASEEILGSVDGFKFFRGILKFRG")
    question = Text.from_str("Inspect the protein sequence and offer a concise description of its properties.")
    outputs = pipeline.run(
        protein=protein,
        text=question,
    )
    print(outputs)
    return pipeline

def test_mutation_explanation():
    pipeline = InferencePipeline(
        task="mutation_explanation",
        model="mutaplm",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/checkpoints/demo/mutaplm.pth",
        device="cuda:0"
    )
    # protein = Protein.from_fasta("MQPWHGKAMQRASEAGATAPKASARNARGAPMDPTESPAAPEAALPKAGKFGPARKSGSRQKKSAPDTQERPPVRATGARAKKAPQRAQDTQPSDATSAPGAEGLEPPAAREPALSRAGSCRQRGARCSTKPRPPPGPWDVPSPGLPVSAPILVRRDAAPGASKLRAVLEKLKLSRDDISTAAGMVKGVVDHLLLRLKCDSAFRGVGLLNTGSYYEHVKISAPNEFDVMFKLEVPRIQLEEYSNTRAYYFVKFKRNPKENPLSQFLEGEILSASKMLSKFRKIIKEEINDIKDTDVIMKRKRGGSPAVTLLISEKISVDITLALESKSSWPASTQEGLRIQNWLSAKVRKQLRLKPFYLVPKHAKEGNGFQEETWRLSFSHIEKEILNNHGKSKTCCENKEEKCCRKDCLKLMKYLLEQLKERFKDKKHLDKFSSYHVKTAFFHVCTQNPQDSQWDRKDLGLCFDNCVTYFLQCLRTEKLENYFIPEFNLFSSNLIDKRSKEFLTKQIEYERNNEFPVFDEF")
    # mutation = "D95A"
    protein = Protein.from_fasta("MTLENVLEAARHLHQTLPALSEFGNWPTDLTATGLQPRAIPATPLVQALDQPGSPRTTGLVQAIRSAAHLAHWKRTYTEAEVGADFRNRYGYFELFGPTGHFHSTQLRGYVAYWGAGLDYDWHSHQAEELYLTLAGGAVFKVDGERAFVGAEGTRLHASWQSAAMSTGDQPILTFVLWRGEGLNALPRMDAA")
    mutation = "H163A"
    function = Text.from_str("Able to cleave dimethylsulfonioproprionate (DMSP) in vitro, releasing dimethyl sulfide (DMS). DMS is the principal form by which sulfur is transported from oceans to the atmosphere. The real activity of the protein is however subject to debate and it is unclear whether it constitutes a real dimethylsulfonioproprionate lyase in vivo: the very low activity with DMSP as substrate suggests that DMSP is not its native substrate.")
    outputs = pipeline.run(
        protein=protein,
        mutation=mutation,
        #function=function,
    )
    print(outputs)
    return pipeline

def test_mutation_engineering():
    pipeline = InferencePipeline(
        task="mutation_engineering",
        model="mutaplm",
        model_ckpt="/AIRvePFS/dair/luoyz-data/projects/OpenBioMed/OpenBioMed_arch/checkpoints/demo/mutaplm.pth",
        device="cuda:2"
    )
    protein = Protein.from_fasta("MASDAAAEPSSGVTHPPRYVIGYALAPKKQQSFIQPSLVAQAASRGMDLVPVDASQPLAEQGPFHLLIHALYGDDWRAQLVAFAARHPAVPIVDPPHAIDRLHNRISMLQVVSELDHAADQDSTFGIPSQVVVYDAAALADFGLLAALRFPLIAKPLVADGTAKSHKMSLVYHREGLGKLRPPLVLQEFVNHGGVIFKVYVVGGHVTCVKRRSLPDVSPEDDASAQGSVSFSQVSNLPTERTAEEYYGEKSLEDAVVPPAAFINQIAGGLRRALGLQLFNFDMIRDVRAGDRYLVIDINYFPGYAKMPGYETVLTDFFWEMVHKDGVGNQQEEKGANHVVVK")
    prompt = Text.from_str("Strongly enhanced InsP6 kinase activity. The mutation in the ITPK protein causes a change in its catalytic activity.")
    outputs = pipeline.run(
        protein=protein,
        text=prompt
    )
    print(outputs[0])
    converter = MutationToSequence()
    outputs = converter.run([protein for i in range(len(outputs[0][0]))], outputs[0][0])
    print(outputs[0][0], outputs[1][0])
    return pipeline

def test_protein_generation():
    from open_biomed.models.functional_model_registry import PROTEIN_DECODER_REGISTRY
    from open_biomed.utils.config import Config
    config = Config(config_file="./configs/model/progen.yaml").model
    model = PROTEIN_DECODER_REGISTRY["progen"](config)
    model = model.to("cuda:1")
    print(model.generate_protein()[0])
    protein = Protein.from_fasta('GFLPFRGADEGLAAREAATLAARGTAARAYREDSWAVPVPRGLLGDLTARVAALGAASPPPADPLAVTLDLHHVTAEVALTTVLDAATLVHGQTRVLSAEDAAEAATAAAAATEAYLERLQDFVLFMSASVRVWRRGNAAGATGPEWDQWYTVADRDALGSAPTHLAVLGRQADALCHFVLDRVAWGTCGTPLWSGDEDLGNVVATFAGYADRLATAPRDLIM')
    protein = model.collator([model.featurizer(protein)])
    protein = {
        "input_ids": protein["input_ids"].to("cuda:1"),
        "attention_mask": protein["attention_mask"].to("cuda:1"),
    }
    print(model.generate_loss(protein))


# TODO: support other datasets
def test_molecule_property_prediction():
    OUTPUT_PROMPTS = {
        "BBBP": "The blood-brain barrier penetration of the molecule is {output}",
        "SIDER": "The possibility of the molecule to exhibit the side effects are:\n Hepatobiliary disorders: {output[0]:.4f}\n Metabolism and nutrition disorders: {output[1]:.4f}\nProduct issues: {output[2]:.4f}\nEye disorders: {output[3]:.4f}\nInvestigations: {output[4]:.4f}\nMusculoskeletal and connective tissue disorders: {output[5]:.4f}\nGastrointestinal disorders :{output[6]:.4f}\nSocial circumstances: {output[7]:.4f}\nImmune system disorders: {output[8]:.4f}\nReproductive system and breast disorders: {output[9]:.4f}\nNeoplasms benign, malignant and unspecified (incl cysts and polyps): {output[10]:.4f}\nGeneral disorders and administration site conditions: {output[11]:.4f}\nEndocrine disorders: {output[12]:.4f}\nSurgical and medical procedures: {output[13]:.4f}\nVascular disorders: {output[14]:.4f}\nBlood and lymphatic system disorders: {output[15]:.4f}\nSkin and subcutaneous tissue disorders: {output[16]:.4f}\nCongenital, familial and genetic disorders: {output[17]:.4f}\nInfections and infestations: {output[18]:.4f}\nRespiratory, thoracic and mediastinal disorders: {output[19]:.4f}\nPsychiatric disorders: {output[20]:.4f}\nRenal and urinary disorders: {output[21]:.4f}\nPregnancy, puerperium and perinatal conditions: {output[22]:.4f}\nEar and labyrinth disorders: {output[23]:.4f}\nCardiac disorders: {output[24]:.4f}\nNervous system disorders: {output[25]:.4f}\nInjury, poisoning and procedural complications: {output[26]:.4f}\n"
    }
    pipelines = {}
    for task in OUTPUT_PROMPTS:
        pipelines[task] = InferencePipeline(
            task="molecule_property_prediction",
            model="graphmvp",
            model_ckpt=f"/AIRvePFS/dair/yk-data/projects/OpenBioMed_new/logs/molecule_property_prediction/graphmvp-{task}/train/checkpoints/last.ckpt",
            additional_config=f"./configs/dataset/{task.lower()}.yaml",
            device="cuda:0",
            output_prompt=OUTPUT_PROMPTS[task],
        )
    pipeline = EnsemblePipeline(pipelines)
    input_smiles = "Nc1[nH]c(C(=O)c2ccccc2)c(-c2ccccn2)c1C(=O)c1c[nH]c2ccc(Br)cc12"
    outputs = pipeline.run(
        molecule=Molecule.from_smiles(input_smiles),
        task="BBBP",
    )
    print(outputs)
    return pipeline


def test_protein_folding():
    pipeline = InferencePipeline(
        task="protein_folding",
        model="esmfold",
        model_ckpt="/AIRvePFS/dair/users/ailin/.cache/huggingface/hub/esmfold_v1/pytorch_model.bin",
        device="cuda:2"
    )
    protein = Protein.from_fasta("MASDAAAEPSSGVTHPPRYVIGYALAPKKQQSFIQPSLVAQAASRGMDLVPVDASQPLAEQGPFHLLIHALYGDDWRAQLVAFAARHPAVPIVDPPHAIDRLHNRISMLQVVSELDHAADQDSTFGIPSQVVVYDAAALADFGLLAALRFPLIAKPLVADGTAKSHKMSLVYHREGLGKLRPPLVLQEFVNHGGVIFKVYVVGGHVTCVKRRSLPDVSPEDDASAQGSVSFSQVSNLPTERTAEEYYGEKSLEDAVVPPAAFINQIAGGLRRALGLQLFNFDMIRDVRAGDRYLVIDINYFPGYAKMPGYETVLTDFFWEMVHKDGVGNQQEEKGANHVVVK")
    outputs = pipeline.run(
        protein=protein,
    )
    print(outputs[0][0], outputs[1][0])
    return pipeline

INFERENCE_UNIT_TESTS = {
    "text_based_molecule_editing": test_text_based_molecule_editing,
    "pocket_molecule_docking": test_pocket_molecule_docking,
    "structure_based_drug_design": test_structure_based_drug_design,
    "molecule_question_answering": test_molecule_question_answering,
    "protein_question_answering": test_protein_question_answering,
    "mutation_explanation": test_mutation_explanation,
    "mutation_engineering": test_mutation_engineering,
    "protein_generation": test_protein_generation,
    "molecule_property_prediction": test_molecule_property_prediction,
    "protein_folding": test_protein_folding,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="protein_folding")
    args = parser.parse_args()

    if args.task not in INFERENCE_UNIT_TESTS:
        raise NotImplementedError(f"{args.task} is not currently supported!")
    else:
        INFERENCE_UNIT_TESTS[args.task]()
    