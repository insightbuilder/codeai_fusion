lvim.colorscheme = "default"
vim.cmd [[highlight Comment guifg=#90EE90]]
-- Pyright LSP
require('lspconfig').pyright.setup{}
lvim.builtin.cmp.active = true
-- automatically install python syntax highlighting
lvim.builtin.treesitter.ensure_installed = {
  "python",
}

-- setup formatting
local formatters = require "lvim.lsp.null-ls.formatters"
formatters.setup { { name = "black" }, }

lvim.format_on_save.enabled = true
lvim.format_on_save.pattern = { "*.py" }
-- auto format command for formatting and saving rust files
vim.api.nvim_command("autocmd BufWritePre *.rs lua vim.lsp.buf.format()")
-- autoformat for lua
vim.api.nvim_command("autocmd BufWritePre *.lua lua vim.lsp.buf.format()")

-- setup linting
local linters = require "lvim.lsp.null-ls.linters"
linters.setup { { command = "flake8", args = { "--ignore=E203" }, filetypes = { "python" } } }

linters.setup { { command = "pmd", filetypes = { "java" } } }

-- setup debug adapter
lvim.builtin.dap.active = true
local mason_path = vim.fn.glob(vim.fn.stdpath "data" .. "/mason/")
pcall(function()
  require("dap-python").setup(mason_path .. "packages/debugpy/venv/bin/python")
end)

-- Starting Rust configuration taken from <F21>https://github.com/LunarVim/starter.lvim/blob/rust-ide/config.lua
-- if you don't want all the parsers change this to a table of the ones you want
lvim.builtin.treesitter.ensure_installed = {
  "lua",
  "rust",
  "toml",
}

vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "rust_analyzer" })

local codelldb_path = mason_path .. "bin/codelldb"
local liblldb_path = mason_path .. "packages/codelldb/extension/lldb/lib/liblldb"

pcall(function()
  require("rust-tools").setup {
    tools = {
      executor = require("rust-tools/executors").termopen, -- can be quickfix or termopen
      reload_workspace_from_cargo_toml = true,
      runnables = {
        use_telescope = true,
      },
      inlay_hints = {
        auto = true,
        only_current_line = false,
        show_parameter_hints = true,
        parameter_hints_prefix = "<-",
        -- other_hints_prefix show the type details
        other_hints_prefix = "=>",
        max_len_align = false,
        max_len_align_padding = 1,
        right_align = false,
        right_align_padding = 7,
        highlight = "Comment",
      },
      hover_actions = {
        border = "rounded",
      },
      on_initialized = function()
        vim.api.nvim_create_autocmd({ "BufWritePost", "BufEnter", "CursorHold", "InsertLeave" }, {
          pattern = { "*.rs" },
          callback = function()
            local _, _ = pcall(vim.lsp.codelens.refresh)
          end,
        })
      end,
    },
    dap = {
      -- adapter= codelldb_adapter,
      adapter = require("rust-tools.dap").get_codelldb_adapter(codelldb_path, liblldb_path),
    },
    server = {
      on_attach = function(client, bufnr)
        require("lvim.lsp").common_on_attach(client, bufnr)
        local rt = require "rust-tools"
        vim.keymap.set("n", "K", rt.hover_actions.hover_actions, { buffer = bufnr })
      end,

      capabilities = require("lvim.lsp").common_capabilities(),
      settings = {
        ["rust-analyzer"] = {
          lens = {
            enable = true,
          },
          checkOnSave = {
            enable = true,
            command = "clippy",
          },
          rustfmt = {
            enableRangeFormatting = true
          },
        },
      },
    },
  }
end)

vim.api.nvim_set_keymap("n", "<m-d>", "<cmd>RustOpenExternalDocs<Cr>", { noremap = true, silent = true })

lvim.builtin.which_key.mappings["C"] = {
  name = "Rust",
  r = { "<cmd>RustRunnables<Cr>", "Runnables" },
  t = { "<cmd>lua _CARGO_TEST()<cr>", "Cargo Test" },
  m = { "<cmd>RustExpandMacro<Cr>", "Expand Macro" },
  c = { "<cmd>RustOpenCargo<Cr>", "Open Cargo" },
  p = { "<cmd>RustParentModule<Cr>", "Parent Module" },
  d = { "<cmd>RustDebuggables<Cr>", "Debuggables" },
  v = { "<cmd>RustViewCrateGraph<Cr>", "View Crate Graph" },
  R = {
    "<cmd>lua require('rust-tools/workspace_refresh')._reload_workspace_from_cargo_toml()<Cr>",
    "Reload Workspace",
  },
  o = { "<cmd>RustOpenExternalDocs<Cr>", "Open External Docs" },
  y = { "<cmd>lua require'crates'.open_repository()<cr>", "[crates] open repository" },
  P = { "<cmd>lua require'crates'.show_popup()<cr>", "[crates] show popup" },
  i = { "<cmd>lua require'crates'.show_crate_popup()<cr>", "[crates] show info" },
  f = { "<cmd>lua require'crates'.show_features_popup()<cr>", "[crates] show features" },
  D = { "<cmd>lua require'crates'.show_dependencies_popup()<cr>", "[crates] show dependencies" },
}

lvim.plugins = {
  {
    "Pocco81/auto-save.nvim",
    config = function()
      require("auto-save").setup()
    end,
  },
  {
    url = "https://git.sr.ht/~whynothugo/lsp_lines.nvim",
    config = function()
      require("lsp_lines").setup()
    end,
  },
  "ChristianChiarulli/swenv.nvim",
  "stevearc/dressing.nvim",
  "mfussenegger/nvim-dap-python",
  "simrat39/rust-tools.nvim",
  "mg979/vim-visual-multi",
  "actionshrimp/vim-xpath",
  {
    "folke/todo-comments.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("todo-comments").setup {
        -- Your custom configuration goes here
        signs = true, -- Show icons in the sign column
        keywords = {
          TODO = { icon = " ", color = "info" },
          FIX = { icon = " ", color = "error" },
          HACK = { icon = " ", color = "warning" },
          WARN = { icon = " ", color = "warning" },
          PERF = { icon = " ", color = "hint" },
          NOTE = { icon = " ", color = "hint" },
        },
      }
    end,
  },
  {
    "saecki/crates.nvim",
    version = "v0.3.0",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("crates").setup {
        null_ls = {
          enabled = true,
          name = "crates.nvim",
        },
        popup = {
          border = "rounded",
        },
      }
    end,
  },

  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      local configs = require("nvim-treesitter.configs")
      configs.setup({
        ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "elixir", "heex", "javascript", "html", "markdown", "rust" },
        sync_install = false,
        highlight = { enable = true },
        indent = { enable = true },
      })
    end
  },
  -- opens file at last edit position
  {
    "ethanholz/nvim-lastplace",
    event = "BufRead",
    config = function()
      require("nvim-lastplace").setup({
        lastplace_ignore_buftype = { "quickfix", "nofile", "help" },
        lastplace_ignore_filetype = {
          "gitcommit", "gitrebase", "svn", "hgcommit",
        },
        lastplace_open_folds = true,
      })
    end,
  },
  -- helps in manage the session by saving and recovering them
  {
    "folke/persistence.nvim",
    event = "BufReadPre", -- this will only start session saving when an actual file was opened
    lazy = "true",
    config = function()
      require("persistence").setup {
        dir = vim.fn.expand(vim.fn.stdpath "config" .. "/session/"),
        options = { "buffers", "curdir", "tabpages", "winsize" },
      }
    end,
  },
  -- provides the outline of the object symbols on the side
  {
    "simrat39/symbols-outline.nvim",
    config = function()
      require('symbols-outline').setup()
    end
  },
  {
    "epwalsh/obsidian.nvim",
    version = "*", -- recommended, use latest release instead of latest commit
    dependencies = {
      -- Required.
      "nvim-lua/plenary.nvim",
    },
    config = function()
      require("obsidian").setup({
        workspaces = {
          {
            name = "personal",
            path = "/data/data/com.termux/files/home/storage/downloads/Vault/personal",
          },
          -- automatically notes folder for dailies are created under
          -- personal directory
          {
            name = "work",
            path = "/data/data/com.termux/files/home/storage/downloads/Vault/work",
            overrides = {
              notes_subdir = "notes",
            },
          },
        },
        notes_subdir = "/personal/notes/dailies",

        log_level = vim.log.levels.INFO,

        -- Optional, completion of wiki links, local markdown links, and tags using nvim-cmp.
        completion = {
          -- Set to false to disable completion.
          nvim_cmp = true,
          -- Trigger completion at 2 chars.
          min_chars = 2,
        },
        -- Optional, configure key mappings. These are the defaults. If you don't want to set any keymappings this
        -- way then set 'mappings = {}'.
        mappings = {
          -- Overrides the 'gf' mapping to work on markdown/wiki links within your vault.
          ["gf"] = {
            action = function()
              return require("obsidian").util.gf_passthrough()
            end,
            opts = { noremap = false, expr = true, buffer = true },
          },
          -- Toggle check-boxes.
          ["<leader>ch"] = {
            action = function()
              return require("obsidian").util.toggle_checkbox()
            end,
            opts = { buffer = true },
          },
          -- Smart action depending on context, either follow link or toggle checkbox.
          ["<cr>"] = {
            action = function()
              return require("obsidian").util.smart_action()
            end,
            opts = { buffer = true, expr = true },
          }
        },

        ui = {
          enable = true,          -- set to false to disable all additional syntax features
          update_debounce = 200,  -- update delay after a text change (in milliseconds)
          max_file_length = 5000, -- disable UI features for files with more than this many lines
          -- Define how various check-boxes are displayed
          checkboxes = {
            -- NOTE: the 'char' value has to be a single character, and the highlight groups are defined below.
            [" "] = { char = "󰄱", hl_group = "ObsidianTodo" },
            ["x"] = { char = "", hl_group = "ObsidianDone" },
            [">"] = { char = "", hl_group = "ObsidianRightArrow" },
            ["~"] = { char = "󰰱", hl_group = "ObsidianTilde" },
            ["!"] = { char = "", hl_group = "ObsidianImportant" },
            -- Replace the above with this if you don't have a patched font:
            -- [" "] = { char = "☐", hl_group = "ObsidianTodo" },
            -- ["x"] = { char = "✔", hl_group = "ObsidianDone" },

            -- You can also add more custom ones...
          },
          -- Use bullet marks for non-checkbox lists.
          bullets = { char = "•", hl_group = "ObsidianBullet" },
          external_link_icon = { char = "", hl_group = "ObsidianExtLinkIcon" },
          -- Replace the above with this if you don't have a patched font:
          -- external_link_icon = { char = "", hl_group = "ObsidianExtLinkIcon" },
          reference_text = { hl_group = "ObsidianRefText" },
          highlight_text = { hl_group = "ObsidianHighlightText" },
          tags = { hl_group = "ObsidianTag" },
          block_ids = { hl_group = "ObsidianBlockID" },
          hl_groups = {
            -- The options are passed directly to `vim.api.nvim_set_hl()`. See `:help nvim_set_hl`.
            ObsidianTodo = { bold = true, fg = "#f78c6c" },
            ObsidianDone = { bold = true, fg = "#89ddff" },
            ObsidianRightArrow = { bold = true, fg = "#f78c6c" },
            ObsidianTilde = { bold = true, fg = "#ff5370" },
            ObsidianImportant = { bold = true, fg = "#d73128" },
            ObsidianBullet = { bold = true, fg = "#89ddff" },
            ObsidianRefText = { underline = true, fg = "#c792ea" },
            ObsidianExtLinkIcon = { fg = "#c792ea" },
            ObsidianTag = { italic = true, fg = "#89ddff" },
            ObsidianBlockID = { italic = true, fg = "#89ddff" },
            ObsidianHighlightText = { bg = "#75662e" },
          },
        },
        -- Where to put new notes. Valid options are
        --  * "current_dir" - put new notes in same directory as the current buffer.
        --  * "notes_subdir" - put new notes in the default notes subdirectory.
        new_notes_location = "notes_subdir",
        templates = {
          folder = "/media/uberdev/ddrv/gitFolders/devlancer_projects/vaults/templates",
          date_format = "%Y-%m-%d",
          time_format = "%H:%M",
          -- A map for custom variables, the key should be the variable and the value a function
          substitutions = {},
        },
        -- opening the url
        ---@param url string
        follow_url_func = function(url)
          -- vim.fn.jobstart({ "xdg-open", url })
          vim.ui.open(url)
        end,
        -- opening img
        ---@param img string
        follow_img_func = function(img)
          -- needed to add this line for the path to work
          -- eog is the default image viewer, so trying it
          vim.fn.jobstart({ "eog", img })
          -- vim.ui.open(img)
        end,
        attachments = {
          -- If this is a relative path it will be interpreted as relative to the vault root.
          img_folder = "assets/imgs",
          ---@return string
          img_name_func = function()
            -- prefix name with timestamp
            return string.format("&s-", os.time())
          end,
          -- A function that determines the text to insert in the note when pasting an image.
          ---@param client obsidian.Client
          ---@param path obsidian.Path the absolute path to image
          ---@return string
          img_text_func = function(client, path)
            return string.format("![%s](%s)", path.name, path)
          end,
        }
      })
    end,
  },
}
-- provides a way to show full compile time error

vim.keymap.set(
  "",
  "<Leader>f",
  require("lsp_lines").toggle,
  { desc = "Toggle lsp_lines" }
)

-- folke/persistence is required
lvim.builtin.which_key.mappings["S"] = {
  name = "Session",
  c = { "<cmd>lua require('persistence').load()<cr>", "Restore last session for current dir" },
  l = { "<cmd>lua require('persistence').load({ last = true })<cr>", "Restore last session" },
  Q = { "<cmd>lua require('persistence').stop()<cr>", "Quit without saving session" },
}

-- this is showning the relative number
vim.o.relativenumber = true
vim.o.conceallevel = 1
-- this is remapping the jk to escape  key
vim.api.nvim_set_keymap('i', 'jk', '<ESC>', { noremap = true })
lvim.keys.normal_mode["<F6>"] = ":XPathSearchPrompt"

-- java configuration
-- local formatters = require "lvim.lsp.null-ls.formatters"

formatters.setup {
  {
    command = "clang-format",
    filetypes = { "java" },
    extra_args = { "--style", "Google" },
  }
}
-- obsidian keymaps
-- Keymaps for frequently used Obsidian commands
lvim.keys.normal_mode["<leader>od"] = ":ObsidianDailies<CR>"     -- Open today's daily note (ObsidianDailies)
lvim.keys.normal_mode["<leader>op"] = ":ObsidianPaste<CR>"       -- Paste image from clipboard (ObsidianPasteImg)
lvim.keys.normal_mode["<leader>ot"] = ":ObsidianToday<CR>"       -- Tag current note (ObsidianTag)
lvim.keys.normal_mode["<leader>on"] = ":ObsidianNew<CR>"         -- Create a new note (ObsidianNewNote)
lvim.keys.normal_mode["<leader>os"] = ":ObsidianSearch<CR>"      -- Search in notes (ObsidianSearch)
lvim.keys.normal_mode["<leader>oq"] = ":ObsidianQuickSwitch<CR>" -- Switch to another notes
lvim.keys.normal_mode["<leader>ol"] = ":ObsidianTemplate<CR>"    -- Switch to another notes

-- split buffers for easy operation
lvim.keys.normal_mode["|"] = ":vsplit<CR>"
lvim.keys.normal_mode["_"] = ":split<CR>"
-- The close of split happens by Spc-q

-- reload lvim
-- Set a keymap for reloading LunarVim
vim.api.nvim_set_keymap('n', '<leader>h', ':LvimReload<CR>', { noremap = true, silent = false })
-- setting transparency
lvim.transparent_window = true
-- reload options
reload("user.options")

