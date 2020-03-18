# Copyright 2020 Tencent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import torch.utils.dlpack as dlpack
import unittest
from turbo_transformers.layers.modeling_bert import convert2ft_tensor
import turbo_transformers


class TestDLPack(unittest.TestCase):
    def check_dlpack(self, use_cuda):
        if use_cuda:
            self.test_device = torch.device('cuda:0')
        else:
            torch.set_num_threads(1)
            self.test_device = torch.device('cpu')

        a = torch.rand(size=(4, 3),
                       dtype=torch.float32,
                       device=self.test_device)
        tensor = convert2ft_tensor(a)
        self.assertIsNotNone(tensor)
        b = dlpack.from_dlpack(tensor.to_dlpack())

        self.assertTrue(a.equal(b))
        self.assertTrue(b.cpu().equal(a.cpu()))

    def test_dlpack(self):
        self.check_dlpack(use_cuda=False)
        if torch.cuda.is_available() and \
            turbo_transformers.config.is_with_cuda():
            self.check_dlpack(use_cuda=True)


if __name__ == '__main__':
    unittest.main()
