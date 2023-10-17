import pytest
from dptb.plugins.init_nnsk import InitSKModel
from dptb.plugins.init_dptb import InitDPTBModel
from dptb.nnops.NN2HRK import NN2HRK
from dptb.nnops.apihost import NNSKHost,DPTBHost
from dptb.entrypoints.run import run
from dptb.structure.structure import BaseStruct
import torch
import numpy as np

@pytest.fixture(scope='session', autouse=True)
def root_directory(request):
        return str(request.config.rootdir)



def test_nnsk_nn2hrk(root_directory):

    allbonds_true = torch.tensor([[ 7,  0,  7,  0,  0,  0,  0],
        [ 5,  1,  5,  1,  0,  0,  0],
        [ 7,  0,  5,  1, -1,  0,  0],
        [ 7,  0,  5,  1,  0,  1,  0],
        [ 7,  0,  5,  1,  0,  0,  0]])

    hamil_blocks_true = [torch.tensor([[-0.6769242287,  0.0000000000,  0.0000000000,  0.0000000000],
                                 [ 0.0000000000, -0.2659669220, -0.0000000000, -0.0000000000],
                                 [ 0.0000000000, -0.0000000000, -0.2659669220, -0.0000000000],
                                 [ 0.0000000000, -0.0000000000, -0.0000000000, -0.2659669220]]),
                    torch.tensor([[-0.3448199928,  0.0000000000,  0.0000000000,  0.0000000000],
                            [ 0.0000000000, -0.1364800036, -0.0000000000, -0.0000000000],
                            [ 0.0000000000, -0.0000000000, -0.1364800036, -0.0000000000],
                            [ 0.0000000000, -0.0000000000, -0.0000000000, -0.1364800036]]),
                    torch.tensor([[ 0.1510433108, -0.0613395944,  0.0000000000, -0.1062432900],
                            [ 0.0689922199, -0.0389896892,  0.0000000000,  0.0354437865],
                            [-0.0000000000,  0.0000000000, -0.0594531670,  0.0000000000],
                            [ 0.1194980294,  0.0354437865,  0.0000000000,  0.0019372720]]),
                    torch.tensor([[ 1.5104332566e-01,  1.2267919630e-01,  0.0000000000e+00,-6.1649405581e-09],
                            [-1.3798445463e-01,  2.2400753573e-02,  0.0000000000e+00,-4.1133674245e-09],
                            [-0.0000000000e+00,  0.0000000000e+00, -5.9453174472e-02,0.0000000000e+00],
                            [ 6.9340684306e-09, -4.1133674245e-09,  0.0000000000e+00,-5.9453174472e-02]]),
                    torch.tensor([[ 0.1510433257, -0.0613396056,  0.0000000000,  0.1062432975],
                            [ 0.0689922348, -0.0389896855,  0.0000000000, -0.0354437977],
                            [-0.0000000000,  0.0000000000, -0.0594531745,  0.0000000000],
                            [-0.1194980443, -0.0354437977,  0.0000000000,  0.0019372720]])]
    

    hkmat_true = torch.tensor([[[-6.7692422867e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           4.5312997699e-01+0.0000000000e+00j,
          -3.7252902985e-09+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -5.5578619242e-02+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.4901161194e-08+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.7835950851e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
          -7.4505805969e-09+0.0000000000e+00j,
          -1.4901161194e-08+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -5.5578634143e-02+0.0000000000e+00j],
         [ 4.5312997699e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -7.4505805969e-09+0.0000000000e+00j,
          -3.4481999278e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [-3.7252902985e-09+0.0000000000e+00j,
          -5.5578619242e-02+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.4901161194e-08+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.7835950851e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
          -1.4901161194e-08+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -5.5578634143e-02+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j]],

        [[-6.7692422867e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.5104332566e-01-3.3087224502e-24j,
          -1.2267920375e-01-2.2535804561e-17j,
           0.0000000000e+00+0.0000000000e+00j,
           2.1248659492e-01-1.3011050591e-17j],
         [ 0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           1.3798446953e-01+2.5347333561e-17j,
          -2.2400749847e-02-7.5181610423e-18j,
           0.0000000000e+00+0.0000000000e+00j,
          -7.0887580514e-02+4.3406124800e-18j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           5.9453167021e-02+8.2718061255e-25j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -2.6596692204e-01+0.0000000000e+00j,
          -2.3899608850e-01+1.4634287491e-17j,
          -7.0887580514e-02+4.3406124800e-18j,
           0.0000000000e+00+0.0000000000e+00j,
           5.9453174472e-02+7.5181618694e-18j],
         [-1.5104332566e-01+3.3087224502e-24j,
           1.3798446953e-01-2.5347333561e-17j,
           0.0000000000e+00+0.0000000000e+00j,
          -2.3899608850e-01-1.4634287491e-17j,
          -3.4481999278e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [-1.2267920375e-01+2.2535804561e-17j,
          -2.2400749847e-02+7.5181610423e-18j,
           0.0000000000e+00+0.0000000000e+00j,
          -7.0887580514e-02-4.3406124800e-18j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           5.9453167021e-02-8.2718061255e-25j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j],
         [ 2.1248659492e-01+1.3011050591e-17j,
          -7.0887580514e-02-4.3406124800e-18j,
           0.0000000000e+00+0.0000000000e+00j,
           5.9453174472e-02-7.5181618694e-18j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
           0.0000000000e+00+0.0000000000e+00j,
          -1.3648000360e-01+0.0000000000e+00j]]])
    
    eigenvalues_true = np.array([[-27.033615 , -10.638821 ,  -7.797419 ,  -7.7974143,  -3.1536958,
         -3.1536944,  -0.7693957,  -0.312297 ],
       [-22.924177 , -14.165403 ,  -7.9399633,  -7.867427 ,  -3.712445 ,
         -3.0836837,  -3.0111492,   2.0478976]], dtype=np.float32)
    EF_true = -5.754929542541504
    
    checkfile = f'{root_directory}/dptb/tests/data/hBN/checkpoint/best_nnsk.pth'
    structname = f'{root_directory}/dptb/tests/data/hBN/hBN.vasp'

    proj_atom_anglr_m = {"N":["s","p"],"B":["s","p"]}
    proj_atom_neles = {"N":5,"B":3}
    CutOff =2
    kpoints_list = np.array([[0, 0, 0], [0.5, 0.5, 0.5]])

    with torch.no_grad():
        nnskapi = NNSKHost(checkpoint=checkfile)
        nnskapi.register_plugin(InitSKModel())
        nnskapi.build()
        nhrk = NN2HRK(apihost=nnskapi, mode='nnsk')

        struct = BaseStruct(atom=structname,format='vasp', onsitemode = nnskapi.model_config['onsitemode'],
            cutoff=CutOff,proj_atom_anglr_m=proj_atom_anglr_m,proj_atom_neles=proj_atom_neles)
        _, _ = struct.get_bond()

        nhrk.update_struct(struct)
        allbonds, hamil_blocks, overlap_blocks  = nhrk.get_HR()

        assert  overlap_blocks is None
        assert torch.equal(allbonds, allbonds_true)
        assert len(hamil_blocks) == len(hamil_blocks_true)
        for i in range(len(hamil_blocks)):
            assert (hamil_blocks[i] - hamil_blocks_true[i] < 1e-8).all()
        
        hkmat, skmat = nhrk.get_HK(kpoints = kpoints_list)

        assert (torch.abs(hkmat - hkmat_true) < 1e-8).all()
        assert hkmat.shape == skmat.shape
        assert hkmat.shape == (2, 8, 8)

        skmat_true = torch.eye(8, dtype=torch.complex64).unsqueeze(0).repeat(2, 1, 1)
        assert (torch.abs(skmat - skmat_true) < 1e-8).all()

        eigenvalues,EF = nhrk.get_eigenvalues(kpoints = kpoints_list)

        assert (eigenvalues_true - eigenvalues < 1e-5).all()
        assert (EF_true - EF < 1e-5).all()

        eigenvalues,EF, eigvecks = nhrk.get_eigenvalues(kpoints = kpoints_list,if_eigvec = True)

        assert (eigenvalues_true - eigenvalues < 1e-5).all()
        assert (EF_true - EF < 1e-5).all()
        assert eigvecks.shape == (2, 8, 8)


def test_nnsk_nn2hrk_nrl(root_directory):
    allbonds_true = torch.tensor([[14,  0, 14,  0,  0,  0,  0],
        [14,  1, 14,  1,  0,  0,  0],
        [14,  0, 14,  1, -1,  0,  0],
        [14,  0, 14,  1,  0, -1,  0],
        [14,  0, 14,  1,  0,  0,  0],
        [14,  0, 14,  1,  0,  0, -1]])
    
    hamil_blocks_true = [torch.tensor([[-0.1307418197,  0.0000000000,  0.0000000000,  0.0000000000],
                                 [ 0.0000000000,  0.4017920196,  0.0000000000,  0.0000000000],
                                 [ 0.0000000000,  0.0000000000,  0.4017920196,  0.0000000000],
                                 [ 0.0000000000,  0.0000000000,  0.0000000000,  0.4017920196]]),
                         torch.tensor([[-0.1307418197,  0.0000000000,  0.0000000000,  0.0000000000],
                                 [ 0.0000000000,  0.4017920196,  0.0000000000,  0.0000000000],
                                 [ 0.0000000000,  0.0000000000,  0.4017920196,  0.0000000000],
                                 [ 0.0000000000,  0.0000000000,  0.0000000000,  0.4017920196]]),
                         torch.tensor([[-0.1368636191, -0.0580061898, -0.0580061898,  0.0580061898],
                                 [ 0.0580061898, -0.0047929958,  0.0556640439, -0.0556640439],
                                 [ 0.0580061898,  0.0556640439, -0.0047929958, -0.0556640439],
                                 [-0.0580061898, -0.0556640439, -0.0556640439, -0.0047929958]]),
                         torch.tensor([[-0.1368636191,  0.0580061898, -0.0580061898, -0.0580061898],
                                 [-0.0580061898, -0.0047929958, -0.0556640439, -0.0556640439],
                                 [ 0.0580061898, -0.0556640439, -0.0047929958,  0.0556640439],
                                 [ 0.0580061898, -0.0556640439,  0.0556640439, -0.0047929958]]),
                         torch.tensor([[-0.1368636191,  0.0580061898,  0.0580061898,  0.0580061898],
                                 [-0.0580061898, -0.0047929958,  0.0556640439,  0.0556640439],
                                 [-0.0580061898,  0.0556640439, -0.0047929958,  0.0556640439],
                                 [-0.0580061898,  0.0556640439,  0.0556640439, -0.0047929958]]),
                         torch.tensor([[-0.1368636191, -0.0580061898,  0.0580061898, -0.0580061898],
                                 [ 0.0580061898, -0.0047929958, -0.0556640439,  0.0556640439],
                                 [-0.0580061898, -0.0556640439, -0.0047929958, -0.0556640439],
                                 [ 0.0580061898,  0.0556640439, -0.0556640439, -0.0047929958]])]

    overlap_blocks_true = [torch.tensor([[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [0., 0., 0., 1.]]),
                           torch.tensor([[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [0., 0., 0., 1.]]),
                           torch.tensor([[ 0.1397575587,  0.1073209718,  0.1073209718, -0.1073209718],
                                   [-0.1073209718, -0.0225201398, -0.0961020365,  0.0961020365],
                                   [-0.1073209718, -0.0961020365, -0.0225201398,  0.0961020365],
                                   [ 0.1073209718,  0.0961020365,  0.0961020365, -0.0225201398]]),
                           torch.tensor([[ 0.1397575587, -0.1073209718,  0.1073209718,  0.1073209718],
                                   [ 0.1073209718, -0.0225201398,  0.0961020365,  0.0961020365],
                                   [-0.1073209718,  0.0961020365, -0.0225201398, -0.0961020365],
                                   [-0.1073209718,  0.0961020365, -0.0961020365, -0.0225201398]]),
                           torch.tensor([[ 0.1397575587, -0.1073209718, -0.1073209718, -0.1073209718],
                                   [ 0.1073209718, -0.0225201398, -0.0961020365, -0.0961020365],
                                   [ 0.1073209718, -0.0961020365, -0.0225201398, -0.0961020365],
                                   [ 0.1073209718, -0.0961020365, -0.0961020365, -0.0225201398]]),
                           torch.tensor([[ 0.1397575587,  0.1073209718, -0.1073209718,  0.1073209718],
                                   [-0.1073209718, -0.0225201398,  0.0961020365, -0.0961020365],
                                   [ 0.1073209718,  0.0961020365, -0.0225201398,  0.0961020365],
                                   [-0.1073209718, -0.0961020365,  0.0961020365, -0.0225201398]])]

    hkmat_true = torch.tensor([[[-0.1307418197+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.5474544764+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0191719830+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.4017920196+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.0191719830+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0191719830+0.0000000000e+00j],
         [-0.5474544764+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.1307418197+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j, -0.0191719830+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.0191719830+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.4017920196+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0191719830+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j]],

        [[-0.1307418197+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.2737272382-5.0282880069e-17j,  0.1160123795-7.1037096410e-18j,
           0.1160123721-7.1037096410e-18j,  0.1160123795-7.1037096410e-18j],
         [ 0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.1160123795+7.1037096410e-18j,  0.0095859915-1.7609182180e-18j,
           0.1113280877-6.8168798005e-18j,  0.1113280803-6.8168798005e-18j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.4017920196+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.1160123721+7.1037096410e-18j,  0.1113280877-6.8168798005e-18j,
           0.0095859915-1.7609182180e-18j,  0.1113280877-6.8168798005e-18j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
          -0.1160123795+7.1037096410e-18j,  0.1113280803-6.8168798005e-18j,
           0.1113280877-6.8168798005e-18j,  0.0095859915-1.7609182180e-18j],
         [ 0.2737272382+5.0282880069e-17j, -0.1160123795-7.1037096410e-18j,
          -0.1160123721-7.1037096410e-18j, -0.1160123795-7.1037096410e-18j,
          -0.1307418197+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.1160123795+7.1037096410e-18j,  0.0095859915+1.7609182180e-18j,
           0.1113280877+6.8168798005e-18j,  0.1113280803+6.8168798005e-18j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.1160123721+7.1037096410e-18j,  0.1113280877+6.8168798005e-18j,
           0.0095859915+1.7609182180e-18j,  0.1113280877+6.8168798005e-18j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.4017920196+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.1160123795+7.1037096410e-18j,  0.1113280803+6.8168798005e-18j,
           0.1113280877+6.8168798005e-18j,  0.0095859915+1.7609182180e-18j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.4017920196+0.0000000000e+00j]]])
    
    skmat_true = torch.tensor([[[ 1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.5590302348+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0900805593+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.0900805593+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0900805593+0.0000000000e+00j],
         [ 0.5590302348+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j, -0.0900805593+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.0900805593+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j, -0.0900805593+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j]],

        [[ 1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
          -0.2795151174+5.1346098324e-17j, -0.2146419436+1.3143028912e-17j,
          -0.2146419585+1.3143028912e-17j, -0.2146419436+1.3143028912e-17j],
         [ 0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.2146419436-1.3143028912e-17j,  0.0450402796-8.2737657164e-18j,
          -0.1922040731+1.1769105903e-17j, -0.1922040880+1.1769105903e-17j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.2146419585-1.3143028912e-17j, -0.1922040731+1.1769105903e-17j,
           0.0450402796-8.2737657164e-18j, -0.1922040731+1.1769105903e-17j],
         [ 0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.2146419436-1.3143028912e-17j, -0.1922040880+1.1769105903e-17j,
          -0.1922040731+1.1769105903e-17j,  0.0450402796-8.2737657164e-18j],
         [-0.2795151174-5.1346098324e-17j,  0.2146419436+1.3143028912e-17j,
           0.2146419585+1.3143028912e-17j,  0.2146419436+1.3143028912e-17j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [-0.2146419436-1.3143028912e-17j,  0.0450402796+8.2737657164e-18j,
          -0.1922040731-1.1769105903e-17j, -0.1922040880-1.1769105903e-17j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [-0.2146419585-1.3143028912e-17j, -0.1922040731-1.1769105903e-17j,
           0.0450402796+8.2737657164e-18j, -0.1922040731-1.1769105903e-17j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           1.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j],
         [-0.2146419436-1.3143028912e-17j, -0.1922040880-1.1769105903e-17j,
          -0.1922040731-1.1769105903e-17j,  0.0450402796+8.2737657164e-18j,
           0.0000000000+0.0000000000e+00j,  0.0000000000+0.0000000000e+00j,
           0.0000000000+0.0000000000e+00j,  1.0000000000+0.0000000000e+00j]]])
    
    eigenvalues_true = np.array([[-5.918621  ,  5.254193  ,  5.2541933 ,  5.2541933 ,  5.7211637 ,
         5.721164  ,  5.7211647 , 12.857235  ],
       [-4.383606  , -0.44771674,  3.2995718 ,  3.299575  ,  8.068163  ,
         8.981795  ,  8.981799  , 17.727243  ]], dtype=np.float32)
    EF_true = 5.487678527832031
    
    checkfile = f'{root_directory}/examples/NRL-TB/silicon/ckpt/nrl_ckpt.pth'
    proj_atom_anglr_m = {"Si":["3s","3p"]}
    proj_atom_neles = {"Si":4}
    CutOff = 3
    kpoints_list = np.array([[0, 0, 0], [0.5, 0.5, 0.5]])
    structname = f'{root_directory}/examples/NRL-TB/silicon/data/silicon.vasp'
    struct = BaseStruct(atom=structname,format='vasp', onsitemode = 'NRL',
            cutoff=CutOff,proj_atom_anglr_m=proj_atom_anglr_m,proj_atom_neles=proj_atom_neles)
    _, _ = struct.get_bond()

    with torch.no_grad():
        nnskapi = NNSKHost(checkpoint=checkfile)
        nnskapi.register_plugin(InitSKModel())
        nnskapi.build()
        nhrk = NN2HRK(apihost=nnskapi, mode='nnsk')
        nhrk.update_struct(struct)
        allbonds, hamil_blocks, overlap_blocks  = nhrk.get_HR()

        assert torch.equal(allbonds, allbonds_true) 
        assert len(hamil_blocks) == len(hamil_blocks_true)
        assert len(overlap_blocks) == len(overlap_blocks_true)
        assert len(hamil_blocks) == len(overlap_blocks)
        for i in range(len(hamil_blocks)):
            assert (hamil_blocks[i] - hamil_blocks_true[i] < 1e-8).all()
            assert (overlap_blocks[i] - overlap_blocks_true[i] < 1e-8).all()

        hkmat, skmat = nhrk.get_HK(kpoints = kpoints_list)

        assert (torch.abs(hkmat - hkmat_true) < 1e-8).all()
        assert (torch.abs(skmat - skmat_true) < 1e-8).all()
        assert hkmat.shape == skmat.shape
        assert hkmat.shape == (2, 8, 8)

        eigenvalues,EF = nhrk.get_eigenvalues(kpoints = kpoints_list)

        assert (eigenvalues_true - eigenvalues < 1e-5).all()
        assert (EF_true - EF < 1e-5).all()

        eigenvalues,EF, eigvecks = nhrk.get_eigenvalues(kpoints = kpoints_list,if_eigvec = True)

        assert (eigenvalues_true - eigenvalues < 1e-5).all()
        assert (EF_true - EF < 1e-5).all()
        assert eigvecks.shape == (2, 8, 8)


