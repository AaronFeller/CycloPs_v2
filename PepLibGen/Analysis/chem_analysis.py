#!/usr/bin/env python
"""
Chemical data about a molecule.

Molecules are defined by SMILES strings. Can work out logP values, Lipinski's 
rules, etc...

Uses rdkit
"""

from rdkit import Chem

# from rdkit.Chem import AllChem
from rdkit.Chem import Crippen
from rdkit.Chem import Lipinski
from rdkit.Chem import Descriptors


class SmilesError(Exception):
    pass


def log_partition_coefficient(smiles):
    """
    Returns the octanol-water partition coefficient given a molecule SMILES
    string
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
    except Exception as e:
        raise SmilesError("%s returns a None molecule" % smiles)

    return Crippen.MolLogP(mol)


def lipinski_trial(smiles):
    """
    Returns which of Lipinski's rules a molecule has failed, or an empty list

    Lipinski's rules are:
    Hydrogen bond donors <= 5
    Hydrogen bond acceptors <= 10
    Molecular weight < 500 daltons
    logP < 5
    """
    passed = []
    failed = []

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise Exception("%s is not a valid SMILES string" % smiles)

    num_hdonors = Lipinski.NumHDonors(mol)
    num_hacceptors = Lipinski.NumHAcceptors(mol)
    mol_weight = Descriptors.MolWt(mol)
    mol_logp = Crippen.MolLogP(mol)

    failed = []

    if num_hdonors > 5:
        failed.append("Over 5 H-bond donors, found %s" % num_hdonors)
    else:
        passed.append("Found %s H-bond donors" % num_hdonors)

    if num_hacceptors > 10:
        failed.append("Over 10 H-bond acceptors, found %s" % num_hacceptors)
    else:
        passed.append("Found %s H-bond acceptors" % num_hacceptors)

    if mol_weight >= 500:
        failed.append("Molecular weight over 500, calculated %s" % mol_weight)
    else:
        passed.append("Molecular weight: %s" % mol_weight)

    if mol_logp >= 5:
        failed.append("Log partition coefficient over 5, calculated %s" % mol_logp)
    else:
        passed.append("Log partition coefficient: %s" % mol_logp)

    return passed, failed


def lipinski_pass(smiles):
    """
    Wraps around lipinski trial, but returns a simple pass/fail True/False
    """
    passed, failed = lipinski_trial(smiles)
    if failed:
        return False
    else:
        return True
