# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STEPS - STochastic Engine for Pathway Simulation
# Copyright (C) 2007-2014 Okinawa Institute of Science and Technology, Japan.
# Copyright (C) 2003-2006 University of Antwerp, Belgium.
#
# See the file AUTHORS for details.
#
# This file is part of STEPS.
#
# STEPS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# STEPS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Modified version for sharing with CUBIT community
# Author: Weiliang Chen (w.chen@oist.jp)

try:
    import cubit
except ImportError:
    print "Unable to import CUBIT module."

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getSelectedVolumes():
    """
    Return the CUBIT indices of mouse selected volumes.
        
    Parameters:
        None
        
    Return:
        cubit_ids
    """
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    idxs = cubit.get_group_volumes(group_id)
    cubit.delete_group(group_id)
    return idxs

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getSelectedSurfaces():
    """
    Return the CUBIT indices of mouse selected surfaces.
        
    Parameters:
        None
        
    Return:
        cubit_ids
    """
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    idxs = cubit.get_group_surfaces(group_id)
    cubit.delete_group(group_id)
    return idxs

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getSelectedNodes():
    """
    Return the CUBIT indices of mouse selected vertex nodes.
        
    Parameters:
        None
        
    Return:
        cubit_ids
    """
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    idxs = cubit.get_group_nodes(group_id)
    cubit.delete_group(group_id)
    return idxs

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getSelectedTets():
    """
    Return the CUBIT indices of mouse selected tetrahedrons.
    
    Parameters:
        None
        
    Return:
        cubit_ids
    """
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    idxs = cubit.get_group_tets(group_id)
    cubit.delete_group(group_id)
    return idxs

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getSelectedTris():
    """
    Return the CUBIT indices of mouse selected triangles.
    
    Parameters:
        None
    
    Return:
        cubit_ids
    """
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    idxs = cubit.get_group_tris(group_id)
    cubit.delete_group(group_id)
    return idxs

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getNodesBoundInPassedVols(target_list, volume_ids):
    """
    Return nodes bound in mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target nodes
                    
    Return:
        List of indices of nodes bound by the volumes
    """
    
    in_list = []
    
    for v in target_list:
        cords = cubit.get_nodal_coordinates(v)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            status = body.point_containment(cords)
            if status == 1 or status == 2:
                in_list.append(v)
                break
    
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getNodesBoundInSelectedVols(target_list):
    """
    Return nodes bound in mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target nodes
                    
    Return:
        List of indices of nodes bound by the volumes
    """
    
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    volume_ids = cubit.get_group_volumes(group_id)
    
    in_list = []
    
    for v in target_list:
        cords = cubit.get_nodal_coordinates(v)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            status = body.point_containment(cords)
            if status == 1 or status == 2:
                in_list.append(v)
                break
    cubit.delete_group(group_id)
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTetsBoundInSelectedVols(target_list):
    """
    Return tetraherons bound in mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target tetrahedrons
                    
    Return:
        List of indices of tetrahedrons bound by the volumes
    """
    
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    volume_ids = cubit.get_group_volumes(group_id)
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tet", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = True
            for cord in cords:
                status = body.point_containment(cord)
                if status == 0:
                    within = False
                    break
            if within:
                in_list.append(t)
                break
    cubit.delete_group(group_id)
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTetsBoundInPassedVols(target_list, volume_ids):
    """
    Return tetraherons bound in mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target tetrahedrons
                    
    Return:
        List of indices of tetrahedrons bound by the volumes
    """
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tet", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = True
            for cord in cords:
                status = body.point_containment(cord)
                if status == 0:
                    within = False
                    break
            if within:
                in_list.append(t)
                break

    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTrisBoundInSelectedVols(target_list):
    """
    Return triangles bound in mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target triangles
                    
    Return:
        List of indices of triangles bound by the volumes
    """
    
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    volume_ids = cubit.get_group_volumes(group_id)
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tri", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = True
            for cord in cords:
                status = body.point_containment(cord)
                if status == 0:
                    within = False
                    break
            if within:
                in_list.append(t)
                break
    cubit.delete_group(group_id)
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTetsOverlapPassedVols(target_list, volume_ids):
    """
    Return tetraherons overlap with mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target tetrahedrons
                    
    Return:
        List of indices of tetrahedrons overlap with the volumes
    """
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tet", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = False
            for cord in cords:
                status = body.point_containment(cord)
                if status == 1:
                    within = True
                    break
            if within:
                in_list.append(t)
                break
    
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTetsOverlapSelectedVols(target_list):
    """
    Return tetraherons overlap with mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target tetrahedrons
                    
    Return:
        List of indices of tetrahedrons overlap with the volumes
    """
    
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    volume_ids = cubit.get_group_volumes(group_id)
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tet", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = False
            for cord in cords:
                status = body.point_containment(cord)
                if status == 1:
                    within = True
                    break
            if within:
                in_list.append(t)
                break
    cubit.delete_group(group_id)
    return in_list

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################

def getTrisOverlapSelectedVols(target_list):
    """
    Return triangles overlap with mouse selected CUBIT volumes.
        
    Parameters:
        * target_list List of indices of target triangles
                    
    Return:
        List of indices of triangles overlap with the volumes
    """
    
    group_id = cubit.create_new_group()
    cubit.silent_cmd("group %i add selection" % (group_id))
    volume_ids = cubit.get_group_volumes(group_id)
    
    in_list = []
    
    for t in target_list:
        verts = cubit.get_connectivity("tri", t)
        cords = []
        for v in verts:
            c = cubit.get_nodal_coordinates(v)
            cords.append(c)
        for vol_id in volume_ids:
            volume = cubit.volume(vol_id)
            body = volume.bodies()[0]
            within = False
            for cord in cords:
                status = body.point_containment(cord)
                if status == 1:
                    within = True
                    break
            if within:
                in_list.append(t)
                break
    cubit.delete_group(group_id)
    return in_list
    
################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
################################################################################

def toStr(e_list):
    """
    Convert entities list to a text string.
        
    Parameters:
        * e_list      entity index list
        
    Return:
        String of the entities separated by comma
    """
    return_str = ""
    for e in e_list:
        return_str += "%i," % (e)
    return return_str

################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
################################################################################
