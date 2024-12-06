from parsing.definitions import ExternalSymbol
from parsing.module import ExternalLibraryModule
from parsing.typing import ArrayType, FunctionArgumentForType, FunctionType, PrimitiveType



class ExternalLibs:
    external_libs = {
        'netcdf': ExternalLibraryModule('netcdf', []),
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
        ]),
    }

    @staticmethod
    def is_external(name):
        return name in ExternalLibs.external_libs
    
    @staticmethod
    def get_module(name):
        return ExternalLibs.external_libs[name]
