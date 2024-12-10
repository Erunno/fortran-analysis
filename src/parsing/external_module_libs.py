from parsing.definitions import ExternalSymbol
from parsing.module import ExternalLibraryModule
from parsing.typing import AnyType, ArrayType, FunctionArgumentForType, FunctionType, PrimitiveType



class ExternalLibs:
    external_libs = {
        'netcdf': ExternalLibraryModule('netcdf', [
            ExternalSymbol(
                name='nf90_open',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='path', arg_type=PrimitiveType.get_character_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='mode', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='NF90_NOWRITE',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='nf90_noerr',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='nf90_inq_dimid',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='name', arg_type=PrimitiveType.get_string_instance().with_infinite_length(), is_optional=False),
                        FunctionArgumentForType(name='dimid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='nf90_inquire_dimension',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='dimid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='len', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='nf90_inq_varid',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='name', arg_type=PrimitiveType.get_string_instance().with_infinite_length(), is_optional=False),
                        FunctionArgumentForType(name='varid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='nf90_strerror',
                type=FunctionType(
                    return_type=PrimitiveType.get_string_instance().with_infinite_length(),
                    arg_types=[
                        FunctionArgumentForType(name='ncerr', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='nf90_close',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
                    ]
                )
            ),
            ExternalSymbol(
                name='nf90_get_var',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='ncid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='varid', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='start', arg_type=ArrayType(
                            element_type=PrimitiveType.get_real_instance().with_any_kind(), 
                            dimensions=[ArrayType.variable_length()]), is_optional=False),
                        
                        FunctionArgumentForType(name='count', arg_type=ArrayType(
                            element_type=PrimitiveType.get_integer_instance().with_any_kind(), 
                            dimensions=[ArrayType.variable_length()]), is_optional=False),

                        FunctionArgumentForType(name='data', arg_type=ArrayType(
                            element_type=PrimitiveType.get_integer_instance().with_any_kind(), 
                            dimensions=[ArrayType.variable_length()]), is_optional=False),
                    ]
                )
            )
        ]),
        'mpi': ExternalLibraryModule('mpi', [
            ExternalSymbol(
                name='mpi_allreduce',
                type=FunctionType(
                    return_type=None,
                    # e.g. call mpi_allreduce(rlval,rtval,1,mpi_real4,mpi_max,mycomm,mpierr)
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_real_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_real_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_real4',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_integer4',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_logical',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_real8',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_success',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_max',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_min',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_sum',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_bcast',
                type=FunctionType(
                    return_type=None,
                    # e.g. call mpi_bcast(rval, size(rval), mpi_real8, iocpu, mycomm, mpierr)
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_request_null',
                # can be assigned to arrays ¯\_(ツ)_/¯ (e.g. see `req = mpi_request_null` in RegCM/Main/mpplib/mod_mppparam.F90)
                type=AnyType.instance()
            ),
            ExternalSymbol(
                name='mpi_proc_null',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            ExternalSymbol(
                name='mpi_waitall',
                type=FunctionType(
                    return_type=PrimitiveType.get_integer_instance().with_any_kind(),
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(AnyType.instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(AnyType.instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_statuses_ignore',
                type=PrimitiveType.get_integer_instance().with_any_kind()
            ),
            # call mpi_sendrecv(rv1,isize,mpi_real8,icpu1,itag, &
                    #   rv2,isize,mpi_real8,icpu2,itag, &
                    #   cartesian_communicator,mpi_status_ignore,mpierr)
            ExternalSymbol(
                name='mpi_sendrecv',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),

                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),]
                )
            ),
            ExternalSymbol(
                name='mpi_status_ignore',
                type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind())
            ),
            ExternalSymbol(
                name='mpi_statuses_ignore',
                type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind())
            ),
            ExternalSymbol(
                name='mpi_irecv',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_logical_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_isend',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_gatherv',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_gather',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
            ExternalSymbol(
                name='mpi_scatterv',
                type=FunctionType(
                    return_type=None,
                    arg_types=[
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_integer_instance().with_any_kind()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        
                        FunctionArgumentForType(name='<empty>', arg_type=ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),

                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False),
                        FunctionArgumentForType(name='<empty>', arg_type=PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)]
                )
            ),
        ]),
    }

    @staticmethod
    def is_external(name):
        return name in ExternalLibs.external_libs
    
    @staticmethod
    def get_module(name):
        return ExternalLibs.external_libs[name]
