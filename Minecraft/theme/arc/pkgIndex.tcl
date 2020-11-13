 #  Arc Ttk Theme - Modification for Minecraft

#  Copyright (c) 2020 Minecraft Team
#  Copyright (c) 2015 Sergei Golovan <sgolovan@nes.ru>

#  This file is part of Arc
#  Arc is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  Arc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with Arc.  If not, see <http://www.gnu.org/licenses/>.

if {![file isdirectory [file join $dir arc]]} { return }

package ifneeded ttk::theme::arc 0.1 \
    [list source [file join $dir arc.tcl]]
