
import torch
import torch.nn as nn

class ConvLSTMCell(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size, bias=True):
        super().__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv2d(input_dim + hidden_dim, 4 * hidden_dim,
                              kernel_size, padding=padding, bias=bias)
        self.hidden_dim = hidden_dim

    def forward(self, x, hidden_state):
        h_cur, c_cur = hidden_state
        combined = torch.cat([x, h_cur], dim=1)
        conv_output = self.conv(combined)
        (cc_i, cc_f, cc_o, cc_g) = torch.split(conv_output, self.hidden_dim, dim=1)
        i = torch.sigmoid(cc_i)
        f = torch.sigmoid(cc_f)
        o = torch.sigmoid(cc_o)
        g = torch.tanh(cc_g)
        c_next = f * c_cur + i * g
        h_next = o * torch.tanh(c_next)
        return h_next, c_next


class ConvLSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size, output_dim):
        super().__init__()
        self.cell = ConvLSTMCell(input_dim, hidden_dim, kernel_size)
        self.conv_out = nn.Conv2d(hidden_dim, output_dim, kernel_size=1)

    def forward(self, x):
        # x: [batch, seq_len, channels, H, W]
        b, seq_len, c, h, w = x.size()
        h_t = torch.zeros((b, self.cell.hidden_dim, h, w), device=x.device)
        c_t = torch.zeros_like(h_t)

        for t in range(seq_len):
            h_t, c_t = self.cell(x[:, t], (h_t, c_t))

        out = self.conv_out(h_t)
        return out  # prediction for next timestep


