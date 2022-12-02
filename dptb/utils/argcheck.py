from typing import List, Callable
from dargs import dargs, Argument, Variant, ArgumentEncoder


model_config_checklist = ['dptb-if_batch_normalized', 'dptb-bond_net_type', 'dptb-env_net_type', 'dptb-onsite_net_type', 'dptb-bond_net_activation', 'dptb-env_net_activation', 'dptb-onsite_net_activation', 
                        'dptb-bond_net_neuron', 'dptb-env_net_neuron', 'dptb-onsite_net_neuron', 'dptb-axis_neuron', 'skfunction-skformula', 'sknetwork-sk_onsite_nhidden', 
                        'sknetwork-sk_hop_nhidden']


def common_options():
    doc_device = ""
    doc_dtype = ""
    doc_onsitemode = ""
    doc_onsite_cutoff = ""
    doc_bond_cutoff = ""
    doc_env_cutoff = ""
    doc_sk_file_path = ""
    doc_proj_atom_neles = ""
    doc_proj_atom_anglr_m = ""
    doc_atomtype = ""
    doc_time_symm = ""

    args = [
        Argument("onsite_cutoff", float, optional = False, doc = doc_onsite_cutoff),
        Argument("bond_cutoff", float, optional = False, doc = doc_bond_cutoff),
        Argument("env_cutoff", float, optional = False, doc = doc_env_cutoff),
        Argument("atomtype", list, optional = False, doc = doc_atomtype),
        Argument("proj_atom_neles", dict, optional = False, doc = doc_proj_atom_neles),
        Argument("proj_atom_anglr_m", dict, optional = False, doc = doc_proj_atom_anglr_m),
        Argument("device", str, optional = True, default="cpu", doc = doc_device),
        Argument("dtype", str, optional = True, default="float32", doc = doc_dtype),
        Argument("onsitemode", str, optional = True, default = "none", doc = doc_onsitemode),
        Argument("sk_file_path", str, optional = True, default="./", doc = doc_sk_file_path),
        Argument("time_symm", bool, optional = True, default=True, doc = doc_time_symm)
    ]

    doc_common_options = ""

    return Argument("common_options", dict, sub_fields=args, sub_variants=[], doc=doc_common_options)


def train_options():
    doc_num_epoch = ""
    doc_seed = ""
    doc_save_freq = ""
    doc_validation_freq = ""
    doc_display_freq = ""
    doc_optimizer = ""
    doc_lr_scheduler = ""

    args = [
        Argument("num_epoch", int, optional=False, doc=doc_num_epoch),
        Argument("seed", int, optional=True, default=3982377700, doc=doc_seed),
        Argument("optimizer", dict, sub_fields=[], sub_variants=[optimizer()], doc = doc_optimizer),
        Argument("lr_scheduler", dict, sub_fields=[], sub_variants=[lr_scheduler()], doc = doc_lr_scheduler),
        Argument("save_freq", int, optional=True, default=10, doc=doc_save_freq),
        Argument("validation_freq", int, optional=True, default=10, doc=doc_validation_freq),
        Argument("display_freq", int, optional=True, default=1, doc=doc_display_freq)
    ]

    doc_train_options = ""

    return Argument("train_options", dict, sub_fields=args, sub_variants=[], optional=False, doc=doc_train_options)


def Adam():

    return [
        Argument("lr", float, optional=True, default=1e-3),
        Argument("betas", list, optional=True, default=[0.9, 0.999]),
        Argument("eps", float, optional=True, default=1e-8),
        Argument("weight_decay", float, optional=True, default=0),
        Argument("amsgrad", bool, optional=True, default=False)

    ]

def SGD():

    return [
        Argument("lr", float, optional=True, default=1e-3),
        Argument("momentum", float, optional=True, default=0.),
        Argument("weight_decay", float, optional=True, default=0.),
        Argument("dampening", float, optional=True, default=0.),
        Argument("nesterov", bool, optional=True, default=False)

    ]

def optimizer():
    doc_type = ""

    return Variant("type", [
            Argument("Adam", dict, Adam()),
            Argument("SGD", dict, SGD())
        ],optional=True, default_tag="Adam", doc=doc_type)

def ExponentialLR():

    return [
        Argument("gamma", float, optional=False)
    ]

def lr_scheduler():
    doc_type = ""

    return Variant("type", [
            Argument("Exp", dict, ExponentialLR())
        ],optional=True, default_tag="Exp", doc=doc_type)


def train_data_sub():
    doc_batch_size = ""
    doc_path = ""
    doc_prefix = ""
    
    args = [
        Argument("batch_size", int, optional=False, doc=doc_batch_size),
        Argument("path", str, optional=False, doc=doc_path),
        Argument("prefix", str, optional=False, doc=doc_prefix)
    ]

    doc_train = ""

    return Argument("train", dict, optional=False, sub_fields=args, sub_variants=[], doc=doc_train)

def validation_data_sub():
    doc_batch_size = ""
    doc_path = ""
    doc_prefix = ""
    
    args = [
        Argument("batch_size", int, optional=False, doc=doc_batch_size),
        Argument("path", str, optional=False, doc=doc_path),
        Argument("prefix", str, optional=False, doc=doc_prefix)
    ]

    doc_validation = ""

    return Argument("validation", dict, optional=False, sub_fields=args, sub_variants=[], doc=doc_validation)

def reference_data_sub():
    doc_batch_size = ""
    doc_path = ""
    doc_prefix = ""

    args = [
        Argument("batch_size", int, optional=False, doc=doc_batch_size),
        Argument("path", str, optional=False, doc=doc_path),
        Argument("prefix", str, optional=False, doc=doc_prefix)
    ]

    doc_reference = ""
    
    return Argument("reference", dict, optional=False, sub_fields=args, sub_variants=[], doc=doc_reference)

def data_options():
    doc_use_reference = ""

    args = [Argument("use_reference", bool, optional=False, doc=doc_use_reference),
        train_data_sub(),
        validation_data_sub(),
        reference_data_sub()
    ]

    doc_data_options = ""

    return Argument("data_options", dict, sub_fields=args, sub_variants=[], optional=False, doc=doc_data_options)
        

def sknetwork():
    doc_sk_hop_nhidden = ""
    doc_sk_onsite_nhidden = ""

    args = [
        Argument("sk_hop_nhidden", int, optional=False, doc=doc_sk_hop_nhidden),
        Argument("sk_onsite_nhidden", int, optional=False, doc=doc_sk_onsite_nhidden),
    ]

    doc_sknetwork = ""

    return Argument("sknetwork", dict, optional=True, sub_fields=args, sub_variants=[], default={}, doc=doc_sknetwork)

def skfunction():
    doc_skformula = ""
    doc_sk_cutoff = ""
    doc_sk_decay_w = ""

    args = [
        Argument("skformula", str, optional=True, default="varTang96", doc=doc_skformula),
        Argument("sk_cutoff", float, optional=True, default=6.0, doc=doc_sk_cutoff),
        Argument("sk_decay_w", float, optional=True, default=0.1, doc=doc_sk_decay_w)
    ]

    doc_skfunction = ""

    return Argument("skfunction", dict, optional=True, sub_fields=args, sub_variants=[], default={}, doc=doc_skfunction)

def dptb():
    doc_axis_neuron = ""
    doc_onsite_net_neuron = ""
    doc_env_net_neuron = ""
    doc_bond_net_neuron = ""
    doc_onsite_net_activation = ""
    doc_env_net_activation = ""
    doc_bond_net_activation = "",
    doc_onsite_net_type = ""
    doc_env_net_type = ""
    doc_bond_net_type = ""
    doc_if_batch_normalized = ""

    args = [
        Argument("axis_neuron", int, optional=True, default=10, doc=doc_axis_neuron),
        Argument("onsite_net_neuron", list, optional=True, default=[128, 128, 256, 256], doc=doc_onsite_net_neuron),
        Argument("env_net_neuron", list, optional=True, default=[128, 128, 256, 256], doc=doc_env_net_neuron),
        Argument("bond_net_neuron", list, optional=True, default=[128, 128, 256, 256], doc=doc_bond_net_neuron),
        Argument("onsite_net_activation", str, optional=True, default="tanh", doc=doc_onsite_net_activation),
        Argument("env_net_activation", str, optional=True, default="tanh", doc=doc_env_net_activation),
        Argument("bond_net_activation", str, optional=True, default="tanh", doc=doc_bond_net_activation),
        Argument("onsite_net_type", str, optional=True, default="res", doc=doc_onsite_net_type),
        Argument("env_net_type", str, optional=True, default="res", doc=doc_env_net_type),
        Argument("bond_net_type", str, optional=True, default="res", doc=doc_bond_net_type),
        Argument("if_batch_normalized", bool, optional=True, default=False, doc=doc_if_batch_normalized)
    ]

    doc_dptb = ""

    return Argument("dptb", dict, optional=True, sub_fields=args, sub_variants=[], default={}, doc=doc_dptb)


def model_options():

    doc_model_options = ""

    return Argument("model_options", dict, sub_fields=[skfunction(), sknetwork(), dptb()], sub_variants=[], optional=False, doc=doc_model_options)


def loss_options():
    doc_losstype = ""
    doc_band_min = ""
    doc_band_max = ""
    doc_val_band_min = ""
    doc_val_band_max = ""
    doc_ref_band_min = ""
    doc_ref_band_max = ""
    doc_emin = ""
    doc_emax = ""
    doc_sigma = ""
    doc_numomega = ""
    doc_sortstrength = ""
    doc_gap_penalty = ""
    doc_fermi_band = ""
    doc_loss_gap_eta = ""
    doc_eout_weight = ""

    args = [
        Argument("losstype", str, optional=True, doc=doc_losstype, default='l2eig_deig_sf'),
        Argument("band_min", int, optional=True, doc=doc_band_min, default=0),
        Argument("band_max", [int, None], optional=True, doc=doc_band_max, default=None),
        Argument("val_band_min", [int, None], optional=True, doc=doc_val_band_min, default=None),
        Argument("val_band_max", [int, None], optional=True, doc=doc_val_band_max, default=None),
        Argument("ref_band_min", [int, None], optional=True, doc=doc_ref_band_min, default=None),
        Argument("ref_band_max", [int, None], optional=True, doc=doc_ref_band_max, default=None),
        Argument("emin", [int, None], optional=True, doc=doc_emin,default=None),
        Argument("emax", [int, None], optional=True, doc=doc_emax,default=None),
        Argument("sigma", [int, None], optional=True, doc=doc_sigma, default=None),
        Argument("num_omega", [int, None], optional=True, doc=doc_numomega,default=None),
        Argument("sortstrength", list, optional=True, doc=doc_sortstrength,default=[0.01,0.01]),
        Argument("gap_penalty", bool, optional=True, doc=doc_gap_penalty, default=False),
        Argument("fermi_band", int, optional=True, doc=doc_fermi_band,default=0),
        Argument("loss_gap_eta", float, optional=True, doc=doc_loss_gap_eta, default=0.01),
        Argument("ref_gap_penalty", [bool, None], optional=True, doc=doc_gap_penalty, default=None),
        Argument("ref_fermi_band", [int, None], optional=True, doc=doc_fermi_band,default=None),
        Argument("ref_loss_gap_eta", [float, None], optional=True, doc=doc_loss_gap_eta, default=None),
        Argument("eout_weight", float, optional=True, doc=doc_loss_gap_eta, default=0.),
    ]

    doc_loss_options = ""
    return Argument("loss_options", dict, sub_fields=args, sub_variants=[], optional=False, doc=doc_loss_options)

def normalize(data):

    co = common_options()
    tr = train_options()
    da = data_options()
    mo = model_options()
    lo = loss_options()

    base = Argument("base", dict, [co, tr, da, mo, lo])
    data = base.normalize_value(data)
    # data = base.normalize_value(data, trim_pattern="_*")
    base.check_value(data, strict=True)

    return data
